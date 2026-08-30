from decimal import Decimal

from app.models.document import ExtractedDocument, ExtractedPage
from app.models.enums import Provider, TransactionType
from app.parsers.cdsl import CDSLParser


def test_cdsl_parser_extracts_mutual_fund_folio_valuation_and_sip() -> None:
    document = ExtractedDocument(
        pages=[
            ExtractedPage(
                page_number=1,
                raw_text="""Central Depository Services (India) Limited
CAS ID: TEST123
TEST INVESTOR
Scheme Name : Example Equity Fund - Growth
Folio No : 12345/6
ISIN : INF000A00001
MUTUAL FUND UNITS HELD WITH MF/RTA
Example Equity Fund
ISIN : INF000A00001
10-07-2026 SIP Purchase 500.00 100.00 100.00 5.000
MUTUAL FUND UNITS HELD AS ON
Example Equity Fund - INF000A00001 12345/6 15.000 101.00 1,000.00 1,515.00
""",
            )
        ]
    )

    result = CDSLParser().parse(document)

    assert result.provider == Provider.CDSL
    assert result.investor_name == "TEST INVESTOR"
    scheme = result.folios[0].schemes[0]
    assert result.folios[0].folio_number == "12345/6"
    assert scheme.units == Decimal("15.000")
    assert scheme.nav == Decimal("101.00")
    assert scheme.current_value == Decimal("1515.00")
    assert scheme.transactions[0].type == TransactionType.SIP
    assert scheme.transactions[0].amount == Decimal("500.00")


def test_cdsl_parser_extracts_demat_holdings_and_transactions() -> None:
    pages = [ExtractedPage(page_number=1, raw_text="CAS ID: TEST\nTEST INVESTOR")]
    pages.extend(ExtractedPage(page_number=index, raw_text="") for index in range(2, 7))
    pages.append(
        ExtractedPage(
            page_number=7,
            raw_text="""INE000A00001
10-07-2026 1.000 2.000 -- 3.000
""",
        )
    )
    pages.append(
        ExtractedPage(
            page_number=8,
            raw_text="""EXAMPLE LIMITED
INE000A00001 EQUITY SHARES 3.000 -- -- -- 3.000 100.0000 300.00
""",
        )
    )
    pages.extend(ExtractedPage(page_number=index, raw_text="") for index in range(9, 11))
    document = ExtractedDocument(pages=pages)

    result = CDSLParser().parse(document)

    account = result.demat_accounts[0]
    assert account.holdings[0].isin == "INE000A00001"
    assert account.holdings[0].security_name == "EXAMPLE LIMITED"
    assert account.holdings[0].trading_symbol is None
    assert account.holdings[0].current_value == Decimal("300.00")
    assert account.transactions[0].closing_balance == Decimal("3.000")
