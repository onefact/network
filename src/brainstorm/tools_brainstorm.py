"""
Brainstorming tools. Mishmosh of types atm, just getting it on paper.

Note, these are just copilot tabs atm, none are functional.
"""
# import fuzzywuzzy.process as fuzz
from typing import List, Dict

# SQLite Backend
# Return all facilities from neighboring states
def get_neighboring_state_facilities(state: str, facilities: List[str]) -> List[str]:
    """
    When characterizing a health system, they typically expand within a particular geographic area.
    It may be possible
    """
    return [facility for facility in facilities if facility.endswith(state)]


# Querying External Sources
## Thoroughly inspect website
def inspect_website_for_service_lines(url: str) -> str:
    """
    Thoroughly inspect website, including PDF's, et cetera, that may be hosted on the website.
    Output a list of service lines (Hospital, HHA, Hospice, etc.)

    Note: Many orgs expose documents from their intranet which may be useful to characterize the entities.
    """
    return None

def inspect_website_for_org_structure(url: str) -> str:
    """TODO
    """
    return None


def inspect_website_for_financial_statements(url: str) -> str:
    """TODO
    """
    return None


## Query open corporates data
def query_open_corporates_data(entity: str) -> str:
    """
    Query open corporates data to get a sense of the corporate structure of the entity.
    """
    return None

## Archive External Sources
def save_internet_archive(url: str) -> str:
    """
    Save the internet archive of a website.
    """
    return None


# String Utils
## Extract named entities from a string
def get_ner_str(pdf: str) -> List[str]:
    """
    Extract named entities from a string. Should probably use a named tuple with some types...

    Corporate SEC filings are rich w/r how the org thinks about subcomponents.
    
    Example, see:
    https://www.jeffersonhealth.org/content/dam/health2021/documents/financial/tjuh-financial-statements/tjuh-audited-financial-statements-2023.pdf
    TJUHS, Abington, JHNES, Kennedy, Magee and Einstein are integrated healthcare
    organizations that provide inpatient, outpatient and emergency care services through acute care,
    ambulatory care, rehabilitation care, physician and other primary care services for residents of
    the Greater Philadelphia Region. TJU is the sole corporate member of TJUHS, Abington,
    JHNES, Kennedy, Magee and Einstein. 
    """
    return None


## Compute string similarity between one string and all candidates
def string_similarity(string: str, candidates: List[str]) -> Dict[str, float]:
    """
    Compute string similarity between one string and all candidates, use pydantic
    """ 
    return None # {candidate: fuzz.ratio(string, candidate) for candidate in candidates}
