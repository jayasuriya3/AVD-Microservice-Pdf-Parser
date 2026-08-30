import re
from datetime import datetime
from decimal import Decimal

from app.models.demat import DematAccount, DematHolding, DematTransaction
from app.models.document import ExtractedDocument
from app.models.enums import Provider, TransactionType
from app.models.folio import Folio
from app.models.scheme import Scheme
from app.models.transaction import Transaction
from app.parsers.base import BaseCASParser, ParserMatch, RawCASResult
from app.services.security_master import canonical_security_name, trading_symbol


class CDSLParser(BaseCASParser):
    """Parse direct mutual-fund folios and demat accounts in CDSL CAS documents."""

    provider = Provider.CDSL

    def can_parse(self, document: ExtractedDocument) -> ParserMatch:
        text = document.text.lower()
        matches = "cas id:" in text and ("central depository services" in text or "cdsl" in text)
        return ParserMatch(provider=self.provider, confidence=1 if matches else 0)

    def parse(self, document: ExtractedDocument) -> RawCASResult:
        text = document.text
        investor_name = self._investor_name(text)
        folio_schemes = self._folio_schemes(text)
        valuations = self._valuations(text)
        transactions = self._transactions(text)
        demat_accounts = self._demat_accounts(document)

        folios: list[Folio] = []
        for folio_number, scheme_name in folio_schemes.items():
            valuation = valuations.get(folio_number)
            scheme = Scheme(
                scheme_name_raw=scheme_name,
                units=valuation["units"] if valuation else None,
                nav=valuation["nav"] if valuation else None,
                current_value=valuation["value"] if valuation else None,
                transactions=transactions.get(folio_number, []),
                confidence=Decimal("0.9") if valuation else Decimal("0.6"),
            )
            folios.append(Folio(folio_number=folio_number, schemes=[scheme]))

        warnings: list[str] = []
        if not folios:
            warnings.append("No mutual-fund folios found in CDSL CAS")
        if not demat_accounts:
            warnings.append("No demat accounts found in CDSL CAS")
        return RawCASResult(
            provider=self.provider,
            investor_name=investor_name,
            folios=folios,
            demat_accounts=demat_accounts,
            warnings=warnings,
        )

    @classmethod
    def _demat_accounts(cls, document: ExtractedDocument) -> list[DematAccount]:
        text = document.text
        accounts = [
            DematAccount(
                depository="CDSL",
                dp_name=re.sub(r"\s+", " ", match.group("name")).strip(),
                dp_id=match.group("dp_id"),
                client_id=match.group("client_id"),
            )
            for match in re.finditer(
                r"DP Name\s*:\s*(?P<name>.+?)\s+DP ID\s*:\s*(?P<dp_id>[A-Z0-9]+)\s+"
                r"Client Id\s*:\s*(?P<client_id>[A-Z0-9]+)",
                text,
                flags=re.IGNORECASE,
            )
        ]
        holdings = cls._demat_holdings(document)
        transactions = cls._demat_transactions(document)
        if holdings or transactions:
            target = next((account for account in accounts if account.dp_name and "ZERODHA" in account.dp_name), None)
            if target is None:
                target = DematAccount(depository="CDSL", dp_name="CDSL consolidated account")
                accounts.append(target)
            target.holdings = holdings
            target.transactions = transactions
        return accounts

    @staticmethod
    def _demat_holdings(document: ExtractedDocument) -> list[DematHolding]:
        holding_text = "\n".join(page.raw_text for page in document.pages[7:10])
        row_pattern = re.compile(
            r"(?P<isin>(?<![A-Z0-9])IN[EF][A-Z0-9]{9}(?![A-Z0-9]))(?P<between>[\s\S]{0,250}?)"
            r"(?P<quantity>\d+\.\d+)\s+--\s+--\s+--\s+(?P<free>\d+\.\d+)\s+"
            r"(?P<price>\d+\.\d+)\s+(?P<value>[\d,]+\.\d+)",
        )
        holdings: list[DematHolding] = []
        previous_end = 0
        for match in row_pattern.finditer(holding_text):
            context = holding_text[previous_end:match.start()]
            name_lines = [line.strip() for line in context.splitlines() if line.strip()]
            security_name = " ".join(name_lines[-4:]) or None
            holdings.append(
                DematHolding(
                    isin=match.group("isin"),
                    security_name=canonical_security_name(
                        match.group("isin"),
                        re.sub(r"\s+", " ", security_name) if security_name else None,
                    ),
                    trading_symbol=trading_symbol(match.group("isin")),
                    quantity=Decimal(match.group("quantity")),
                    market_price=Decimal(match.group("price")),
                    current_value=Decimal(match.group("value").replace(",", "")),
                )
            )
            previous_end = match.end()
        bond_text = document.pages[10].raw_text if len(document.pages) > 10 else ""
        bond_pattern = re.compile(
            r"(?P<isin>(?<![A-Z0-9])INE[A-Z0-9]{9}(?![A-Z0-9]))\s+(?P<name>[A-Z]+).*?"
            r"(?P<quantity>\d+\.\d+)\s+[\d,]+\.\d+\s+(?P<price>[\d,]+\.\d+)\s+"
            r"(?P<value>[\d,]+\.\d+)",
        )
        holdings.extend(
            DematHolding(
                isin=match.group("isin"),
                security_name=canonical_security_name(match.group("isin"), match.group("name")),
                trading_symbol=trading_symbol(match.group("isin")),
                quantity=Decimal(match.group("quantity")),
                market_price=Decimal(match.group("price").replace(",", "")),
                current_value=Decimal(match.group("value").replace(",", "")),
            )
            for match in bond_pattern.finditer(bond_text)
        )
        return holdings

    @staticmethod
    def _demat_transactions(document: ExtractedDocument) -> list[DematTransaction]:
        transaction_text = "\n".join(page.raw_text for page in document.pages[6:7])
        transactions: list[DematTransaction] = []
        current_isin: str | None = None
        row_pattern = re.compile(
            r"(?P<date>\d{2}-\d{2}-\d{4})\s+(?P<opening>[\d.]+)\s+"
            r"(?P<credit>[\d.]+|--)\s+(?P<debit>[\d.]+|--)\s+(?P<closing>[\d.]+)",
        )
        for line in transaction_text.splitlines():
            isin = re.search(r"(?<![A-Z0-9])IN[EF][A-Z0-9]{9}(?![A-Z0-9])", line)
            if isin:
                current_isin = isin.group()
            match = row_pattern.search(line)
            if current_isin and match:
                transactions.append(
                    DematTransaction(
                        date=datetime.strptime(match.group("date"), "%d-%m-%Y").date(),
                        isin=current_isin,
                        credit_units=(
                            Decimal(match.group("credit"))
                            if match.group("credit") != "--"
                            else None
                        ),
                        debit_units=(
                            Decimal(match.group("debit"))
                            if match.group("debit") != "--"
                            else None
                        ),
                        closing_balance=Decimal(match.group("closing")),
                    )
                )
        return transactions

    @staticmethod
    def _investor_name(text: str) -> str | None:
        match = re.search(r"CAS ID:\s*[^\n]+\n([^\n]+)", text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _folio_schemes(text: str) -> dict[str, str]:
        records = re.finditer(
            r"Scheme Name\s*:\s*(?P<scheme>.+?)\s*(?:Scheme Code\s*:\s*[^\n]+)?\n"
            r"(?:[^\n]+\n)?Folio No\s*:\s*(?P<folio>[A-Za-z0-9/]+)",
            text,
            flags=re.DOTALL,
        )
        return {
            record.group("folio"): re.sub(r"\s+", " ", record.group("scheme")).strip()
            for record in records
        }

    @staticmethod
    def _valuations(text: str) -> dict[str, dict[str, Decimal]]:
        pattern = re.compile(
            r"(?P<isin>INF[A-Z0-9]+)\s+(?P<folio>[A-Za-z0-9/]+)\s+"
            r"(?P<units>[\d.]+)\s+(?P<nav>[\d.]+)\s+(?P<invested>[\d,.]+)\s+"
            r"(?P<value>[\d,.]+)",
        )
        return {
            match.group("folio"): {
                "units": Decimal(match.group("units")),
                "nav": Decimal(match.group("nav")),
                "value": Decimal(match.group("value").replace(",", "")),
            }
            for match in pattern.finditer(text)
        }

    @staticmethod
    def _transactions(text: str) -> dict[str, list[Transaction]]:
        by_folio: dict[str, list[Transaction]] = {}
        current_folio: str | None = None
        folio_by_isin = {
            match.group("isin"): match.group("folio")
            for match in re.finditer(
                r"Folio No\s*:\s*(?P<folio>[A-Za-z0-9/]+)[\s\S]{0,300}?"
                r"ISIN\s*:\s*(?P<isin>INF[A-Z0-9]+)",
                text,
                flags=re.DOTALL,
            )
        }
        for line in text.splitlines():
            isin = re.search(r"INF[A-Z0-9]+", line)
            if isin:
                current_folio = folio_by_isin.get(isin.group())
                continue
            match = re.search(
                r"(?P<date>\d{2}-\d{2}-\d{4})\s+(?:\S+\s+)*?(?P<amount>[\d,]+\.\d{2})\s+"
                r"(?P<nav>[\d.]+)\s+(?P=nav)\s+(?P<units>[\d.]+)",
                line,
            )
            if current_folio and match:
                by_folio.setdefault(current_folio, []).append(
                    Transaction(
                        date=datetime.strptime(match.group("date"), "%d-%m-%Y").date(),
                        type=TransactionType.SIP,
                        amount=Decimal(match.group("amount").replace(",", "")),
                        nav=Decimal(match.group("nav")),
                        units=Decimal(match.group("units")),
                    )
                )
        return by_folio
