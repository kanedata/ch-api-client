import re
from dataclasses import dataclass, field
from importlib import resources

import httpx2
import pytest
from click.testing import CliRunner
from pytest_httpx2 import HTTPXMock

import ch_api_client.tests.fixtures
from ch_api_client.cli import cli
from ch_api_client.client import COMPANY_API_BASE_URL, DOCUMENT_API_BASE_URL
from ch_api_client.models.company_officer_list import OfficerList, OfficerSummary
from ch_api_client.models.company_profile import CompanyProfile
from ch_api_client.models.document import ContentType, DocumentMetadata
from ch_api_client.models.filing_history import (
    AnnualAccount,
    AnnualAccountList,
    FilingHistoryItem,
    FilingHistoryList,
)
from ch_api_client.models.registered_office_address import RegisteredOfficeAddress
from ch_api_client.models.search import (
    AdvancedCompanySearch,
    AlphabeticalCompanySearch,
    CompanySearch,
    DisqualifiedOfficerSearch,
    DissolvedCompanySearch,
    OfficerSearch,
    Search,
)

DUMMY_API_KEY = "api_key_123456789"


@dataclass
class UrlMock:
    regex: str
    file: str
    base_url: str = COMPANY_API_BASE_URL
    method: str = "GET"

    def _get_content(self) -> bytes:
        return (
            resources.files(ch_api_client.tests.fixtures)
            .joinpath(self.file)
            .read_bytes()
        )

    def _url_regex(self) -> re.Pattern:
        if self.base_url:
            return re.compile(self.base_url + self.regex)
        return re.compile(self.regex)

    def _get_headers(self) -> dict[str, str]:
        auth = httpx2.BasicAuth(DUMMY_API_KEY, "")
        return {"Authorization": auth._auth_header}

    def mock_response(self, httpx2_mock: HTTPXMock):
        httpx2_mock.add_response(
            url=self._url_regex(),
            content=self._get_content(),
            method=self.method,
            match_headers=self._get_headers(),
            is_reusable=True,
        )


@dataclass
class MethodToTest:
    method_name: str
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    url_mocks: list[UrlMock] = field(default_factory=list)
    return_type: type | None = None

    def __str__(self) -> str:
        return f"{self.method_name}[{self.args}-{self.kwargs}]"

    @property
    def cli_command(self):
        return self.method_name.replace("_", "-")

    def add_url_mocks(self, httpx2_mock: HTTPXMock):
        if self.url_mocks:
            for url_mock in self.url_mocks:
                url_mock.mock_response(httpx2_mock)

    def _cli_args(self) -> list[str]:
        args = ["--api-key", DUMMY_API_KEY, self.cli_command, *map(str, self.args)]
        if self.kwargs:
            for key, value in self.kwargs.items():
                if isinstance(value, list):
                    for item in value:
                        args.append(f"--{key.replace('_', '-')}")
                        args.append(str(item))
                else:
                    args.append(f"--{key.replace('_', '-')}")
                    args.append(str(value))
        return args

    def invoke_command(self, runner: CliRunner):
        return runner.invoke(cli, self._cli_args())


METHODS: list[MethodToTest] = [
    MethodToTest(
        method_name="get_company_profile",
        args=["12345678"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})(\?.*)?",
                file="get_company_profile.json",
            ),
        ],
        return_type=CompanyProfile,
    ),
    MethodToTest(
        method_name="get_registered_office_address",
        args=["12345678"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/registered-office-address(\?.*)?",
                file="get_registered_office_address.json",
            ),
        ],
        return_type=RegisteredOfficeAddress,
    ),
    MethodToTest(
        method_name="get_company_officers",
        args=["12345678"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/officers(\?.*)?",
                file="get_company_officers.json",
            ),
        ],
        return_type=OfficerList,
    ),
    MethodToTest(
        method_name="get_company_officer_appointment",
        args=["12345678", "gRlvI3kMYqXmza7tCrs8Mp0UwZc"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/appointments/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_company_officer_appointment.json",
            ),
        ],
        return_type=OfficerSummary,
    ),
    MethodToTest(
        method_name="get_filing_history_list",
        args=["12345678"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/filing-history(\?.*)?",
                file="get_filing_history_list.json",
            ),
        ],
        return_type=FilingHistoryList,
    ),
    MethodToTest(
        method_name="get_annual_account_list",
        args=["12345678"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/filing-history(\?.*)?",
                file="get_filing_history_list.json",
            ),
            UrlMock(
                regex=r"/document/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_document_metadata.json",
                base_url=DOCUMENT_API_BASE_URL,
            ),
        ],
        return_type=AnnualAccountList,
    ),
    MethodToTest(
        method_name="get_annual_account",
        args=["12345678", "2015-01-26"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/filing-history(\?.*)?",
                file="get_filing_history_list.json",
            ),
            UrlMock(
                regex=r"/document/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_document_metadata.json",
                base_url=DOCUMENT_API_BASE_URL,
            ),
        ],
        return_type=AnnualAccount,
    ),
    MethodToTest(
        method_name="get_annual_account_document",
        args=["12345678", "2015-01-26"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/filing-history(\?.*)?",
                file="get_filing_history_list.json",
            ),
            UrlMock(
                regex=r"/document/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_document_metadata.json",
                base_url=DOCUMENT_API_BASE_URL,
            ),
        ],
        return_type=bytes,
    ),
    MethodToTest(
        method_name="get_annual_account_document",
        args=["12345678", "2015-01-26"],
        kwargs={"content_type": ContentType.PDF},
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/filing-history(\?.*)?",
                file="get_filing_history_list.json",
            ),
            UrlMock(
                regex=r"/document/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_document_metadata.json",
                base_url=DOCUMENT_API_BASE_URL,
            ),
        ],
        return_type=bytes,
    ),
    MethodToTest(
        method_name="get_filing_history",
        args=["12345678", "MTc0NKkzZzZ3YWCpcXprY3g"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/filing-history/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_filing_history.json",
            ),
        ],
        return_type=FilingHistoryItem,
    ),
    MethodToTest(
        method_name="get_document_metadata",
        args=["bg01EDBqES8DV0OAqOokaT4Gw8BnplUI4Nm9c4Mzuww"],
        url_mocks=[
            UrlMock(
                regex=r"/document/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_document_metadata.json",
                base_url=DOCUMENT_API_BASE_URL,
            ),
        ],
        return_type=DocumentMetadata,
    ),
    MethodToTest(
        method_name="get_search_all",
        args=["test"],
        url_mocks=[
            UrlMock(regex=r"/search(\?.*)?", file="search.json"),
        ],
        return_type=Search,
    ),
    MethodToTest(
        method_name="get_search_companies",
        args=["test"],
        url_mocks=[
            UrlMock(
                regex=r"/search/companies(\?.*)?",
                file="search_companies.json",
            ),
        ],
        return_type=CompanySearch,
    ),
    MethodToTest(
        method_name="get_search_officers",
        args=["test"],
        url_mocks=[
            UrlMock(
                regex=r"/search/officers(\?.*)?",
                file="search_officers.json",
            ),
        ],
        return_type=OfficerSearch,
    ),
    MethodToTest(
        method_name="get_search_disqualified_officers",
        args=["test"],
        url_mocks=[
            UrlMock(
                regex=r"/search/disqualified-officers(\?.*)?",
                file="search_disqualified-officers.json",
            ),
        ],
        return_type=DisqualifiedOfficerSearch,
    ),
    MethodToTest(
        method_name="get_search_dissolved",
        args=["test", "best-match"],
        url_mocks=[
            UrlMock(
                regex=r"/dissolved-search/companies(\?.*)?",
                file="dissolved-search_companies.json",
            ),
        ],
        return_type=DissolvedCompanySearch,
    ),
    MethodToTest(
        method_name="get_search_alphabetical",
        args=["test"],
        url_mocks=[
            UrlMock(
                regex=r"/alphabetical-search/companies(\?.*)?",
                file="alphabetical-search_companies.json",
            ),
        ],
        return_type=AlphabeticalCompanySearch,
    ),
    MethodToTest(
        method_name="get_search_advanced",
        kwargs={"company_name_includes": "test"},
        url_mocks=[
            UrlMock(
                regex=r"/advanced-search/companies(\?.*)?",
                file="advanced-search_companies.json",
            ),
        ],
        return_type=AdvancedCompanySearch,
    ),
    MethodToTest(
        method_name="get_search_advanced",
        kwargs={"company_name_includes": "test", "company_type": ["ltd", "plc"]},
        url_mocks=[
            UrlMock(
                regex=r"/advanced-search/companies(\?.*)?",
                file="advanced-search_companies.json",
            ),
        ],
        return_type=AdvancedCompanySearch,
    ),
]


@pytest.fixture
def doc_mock(httpx2_mock: HTTPXMock):
    methods = (m for m in METHODS if m.method_name in ("get_document_metadata"))
    for method in methods:
        method.add_url_mocks(httpx2_mock)
    document_url_mock = UrlMock(
        regex=r"/document/([0-9A-Za-z_-]+)/content(\?.*)?",
        file="document.pdf",
        base_url=DOCUMENT_API_BASE_URL,
    )
    document_url_mock.mock_response(httpx2_mock)
    return httpx2_mock
