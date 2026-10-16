from ch_api_client.cli import cli
from ch_api_client.client import CompaniesHouseAPI
from ch_api_client.models.company_officer_list import OfficerList, OfficerSummary
from ch_api_client.models.company_profile import CompanyProfile
from ch_api_client.models.document import DocumentMetadata
from ch_api_client.models.filing_history import (
    AnnualAccount,
    FilingHistoryItem,
    FilingHistoryList,
)
from ch_api_client.models.registered_office_address import RegisteredOfficeAddress
from ch_api_client.models.search import (
    CompanySearch,
    DisqualifiedOfficerSearch,
    OfficerSearch,
    Search,
)


def main() -> None:
    cli()


__all__ = [
    "AnnualAccount",
    "CompaniesHouseAPI",
    "CompanyProfile",
    "CompanySearch",
    "DisqualifiedOfficerSearch",
    "DocumentMetadata",
    "FilingHistoryItem",
    "FilingHistoryList",
    "OfficerList",
    "OfficerSearch",
    "OfficerSummary",
    "RegisteredOfficeAddress",
    "Search",
]
