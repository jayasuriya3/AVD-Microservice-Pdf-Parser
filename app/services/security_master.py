"""Canonical security names keyed by ISIN.

The parser must prefer an ISIN master over PDF layout text.  This in-process
catalogue covers the initial CDSL regression layout; replace it with a versioned
depository/exchange ISIN-master feed as coverage expands.
"""

SECURITY_NAMES: dict[str, str] = {
    "INE885A01032": "Amara Raja Energy & Mobility Limited",
    "INE208A01029": "Ashok Leyland Limited",
    "INE536H01010": "CIE Automotive India Limited",
    "INE059A01026": "Cipla Limited",
    "INE680A01011": "Dhanlaxmi Bank Limited",
    "INE089A01031": "Dr. Reddy's Laboratories Limited",
    "INE532F01054": "Edelweiss Financial Services Limited",
    "INE302A01020": "Exide Industries Limited",
    "INE171A01029": "Federal Bank Limited",
    "INE224A01026": "Greaves Cotton Limited",
    "INE292B01021": "HBL Power Systems Limited",
    "INE040A01034": "HDFC Bank Limited",
    "INE158A01026": "Hero MotoCorp Limited",
    "INF109KC11M9": "ICICI Prudential Nifty Pharma Index Fund - Direct Growth",
    "INE092T01019": "IDFC First Bank Limited",
    "INE095A01012": "IndusInd Bank Limited",
    "INE009A01021": "Infosys Limited",
    "INE379A01028": "ITC Hotels Limited",
    "INE154A01025": "ITC Limited",
    "INE614B01018": "Karnataka Bank Limited",
    "INE522D01027": "Manappuram Finance Limited",
    "INE987B01026": "Natco Pharma Limited",
    "INF204KB17I5": "Nippon India ETF Gold BeES",
    "INF204KC1089": "Nippon India ETF Nifty Pharma",
    "INF204KB15V2": "Nippon India ETF Nifty IT",
    "INE0GGX23010": "PowerGrid Infrastructure Investment Trust",
    "INF879O01100": "Parag Parikh ELSS Tax Saver Fund - Direct Growth",
    "INE775A01035": "Samvardhana Motherson International Limited",
    "INE683A01023": "South Indian Bank Limited",
    "INE668A01016": "Tamilnad Mercantile Bank Limited",
    "INE976I01016": "Tata Capital Limited",
    "INE467B01029": "Tata Consultancy Services Limited",
    "INE1TAE01010": "Tata Motors Limited",
    "INE155A01022": "Tata Motors Passenger Vehicles Limited",
    "INE245A01021": "Tata Power Company Limited",
    "INE081A01020": "Tata Steel Limited",
    "INE142M01025": "Tata Technologies Limited",
    "INE690A01028": "TTK Prestige Limited",
    "INE075A01022": "Wipro Limited",
    "INF0R8F01018": "Zerodha Nifty LargeMidcap 250 Index Fund - Direct Growth",
    "INE010B01027": "Zydus Lifesciences Limited",
}

SECURITY_SYMBOLS: dict[str, str] = {
    "INE885A01032": "AMARAJABAT",
    "INE208A01029": "ASHOKLEY",
    "INE536H01010": "CIEINDIA",
    "INE059A01026": "CIPLA",
    "INE680A01011": "DHANBANK",
    "INE089A01031": "DRREDDY",
    "INE532F01054": "EDELWEISS",
    "INE302A01020": "EXIDEIND",
    "INE171A01029": "FEDERALBNK",
    "INE224A01026": "GREAVESCOT",
    "INE292B01021": "HBLPOWER",
    "INE040A01034": "HDFCBANK",
    "INE158A01026": "HEROMOTOCO",
    "INE092T01019": "IDFCFIRSTB",
    "INE095A01012": "INDUSINDBK",
    "INE009A01021": "INFY",
    "INE379A01028": "ITCHOTELS",
    "INE154A01025": "ITC",
    "INE614B01018": "KARNATAKA",
    "INE522D01027": "MANAPPURAM",
    "INE987B01026": "NATCOPHARM",
    "INF204KB17I5": "GOLDBEES",
    "INF204KC1089": "PHARMABEES",
    "INF204KB15V2": "ITBEES",
    "INE0GGX23010": "PGINVIT",
    "INE775A01035": "MOTHERSON",
    "INE683A01023": "SOUTHBANK",
    "INE668A01016": "TMB",
    "INE976I01016": "TATACAP",
    "INE467B01029": "TCS",
    "INE1TAE01010": "TATAMOTORS",
    "INE155A01022": "TMPV",
    "INE245A01021": "TATAPOWER",
    "INE081A01020": "TATASTEEL",
    "INE142M01025": "TATATECH",
    "INE690A01028": "TTKPRESTIG",
    "INE075A01022": "WIPRO",
    "INE010B01027": "ZYDUSLIFE",
}


def canonical_security_name(isin: str, extracted_name: str | None) -> str | None:
    """Return a canonical ISIN name, never mixed-language PDF layout fragments."""
    if isin in SECURITY_NAMES:
        return SECURITY_NAMES[isin]
    if not extracted_name:
        return None
    ascii_name = "".join(character for character in extracted_name if character.isascii())
    return " ".join(ascii_name.split()) or None


def trading_symbol(isin: str) -> str | None:
    """Return the primary exchange symbol when the security has one."""
    return SECURITY_SYMBOLS.get(isin)
