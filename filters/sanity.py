import re


def sanity_check(title: str, description: str) -> bool:
    """Checks the flat for obious issues in the metadata"""
    return check_title(title) and check_description(description)


BLOCKLIST_KEYWORDS = [
    "wg",
    "wohngemeinschaft",
    "tausch",
    "tauschwohnung",
    "short term",
    "short-term",
    "untermiete",
    "sublet",
    "zwischenmiete",
    "zwischenmieter",
    "kurzzeit",
    "kurzzeitmiete",
    "kurzzeitmieter",
    "sucht",
    "suche",
    "looking for",
]


def check_title(title: str) -> bool:
    """Checks the title for keywords"""
    for keyword in BLOCKLIST_KEYWORDS:
        if keyword in title.lower():
            return False
    dataRangeChecks = [  # TODO
        r"\d{2}\.\d{2}\.\d{4} [-/] \d{2}\.\d{2}\.\d{4}",
        r"\d{2}\.\d{2}\.\d{4}[-/]\d{2}\.\d{2}\.\d{4}",
        r"\d{2}\.\d{2}\.\d{2} [-/] \d{2}\.\d{2}\.\d{2}",
        r"\d{2}\.\d{2}\.\d{2}[-/]\d{2}\.\d{2}\.\d{2}",
        r"\d{2}\.\d{2}\. [-/] \d{2}\.\d{2}\.",
        r"\d{2}\.\d{2}\.[-/]\d{2}\.\d{2}\.",
        r"\d{2}\.\d{2} [-/] \d{2}\.\d{2}",
        r"\d{2}\.\d{2}[-/]\d{2}\.\d{2}",
    ]
    for check in dataRangeChecks:
        if re.search(check, title):
            return False
    return True


def check_description(description: str) -> bool:
    """Checks the description for keywords"""
    # TODO
    return True
