import json
import re
from dataclasses import dataclass, field
from importlib import resources

import httpx2
import pytest
from click.testing import CliRunner
from pytest_httpx2 import HTTPXMock

import ch_api_client.tests.fixtures
from ch_api_client.cli import cli
from ch_api_client.client import (
    COMPANY_API_BASE_URL,
    DOCUMENT_API_BASE_URL,
    CompaniesHouseAPI,
)
from ch_api_client.models.company_officer_list import OfficerList, OfficerSummary
from ch_api_client.models.company_profile import CompanyProfile
from ch_api_client.models.document import DocumentMetadata
from ch_api_client.models.filing_history import FilingHistoryItem, FilingHistoryList
from ch_api_client.models.search import (
    CompanySearch,
    DisqualifiedOfficerSearch,
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

    def invoke_command(self, runner: CliRunner):
        return runner.invoke(
            cli,
            ["--api-key", DUMMY_API_KEY, self.cli_command, *map(str, self.args)],
            **self.kwargs,
        )


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
        args=["12345678", "MTc0NKkzZzZ3YWCpcXprY3g"],
        url_mocks=[
            UrlMock(
                regex=r"/company/([0-9A-Z]{8})/filing-history/([0-9A-Za-z_-]+)(\?.*)?",
                file="get_filing_history.json",
            ),
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
]


@pytest.fixture
def doc_mock(httpx2_mock: HTTPXMock):
    method = next(m for m in METHODS if m.method_name == "get_document_metadata")

    method.add_url_mocks(httpx2_mock)
    document_url_mock = UrlMock(
        regex=r"/document/([0-9A-Za-z_-]+)/content(\?.*)?",
        file="document.pdf",
        base_url=DOCUMENT_API_BASE_URL,
    )
    document_url_mock.mock_response(httpx2_mock)
    return httpx2_mock


def test_ch_api_client_initialization(httpx2_mock: HTTPXMock):
    client = CompaniesHouseAPI(api_key=DUMMY_API_KEY)
    assert client is not None


@pytest.mark.parametrize("method", METHODS, ids=str)
def test_ch_api_client_methods(httpx2_mock: HTTPXMock, method: MethodToTest):
    client = CompaniesHouseAPI(api_key=DUMMY_API_KEY)
    method.add_url_mocks(httpx2_mock)
    client_method = getattr(client, method.method_name)
    result = client_method(*method.args, **method.kwargs)
    assert result is not None
    if method.return_type is not None:
        assert isinstance(result, method.return_type)


def test_ch_api_client_get_document(doc_mock: HTTPXMock):
    client = CompaniesHouseAPI(api_key=DUMMY_API_KEY)
    method = next(m for m in METHODS if m.method_name == "get_document_metadata")

    client_method = getattr(client, method.method_name)
    doc_metadata = client_method(*method.args, **method.kwargs)
    assert doc_metadata is not None
    if method.return_type is not None:
        assert isinstance(doc_metadata, method.return_type)

    document = client.get_document(doc_metadata)
    assert document is not None
    assert isinstance(document, bytes)


@pytest.mark.parametrize("method", METHODS, ids=str)
def test_ch_api_cli(httpx2_mock: HTTPXMock, method: MethodToTest):
    method.add_url_mocks(httpx2_mock)
    runner = CliRunner()
    result = method.invoke_command(runner)
    assert result.exit_code == 0
    split_result = result.output.splitlines()
    for line in split_result:
        assert line is not None
        assert json.loads(line) is not None


def test_ch_api_cli_get_document(doc_mock: HTTPXMock):
    method = next(m for m in METHODS if m.method_name == "get_document_metadata")
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--api-key",
            DUMMY_API_KEY,
            "get-filing-history-document",
            *map(str, method.args),
        ],
        **method.kwargs,
    )
    assert result.exit_code == 0
    assert result.output_bytes is not None
    assert (
        result.output_bytes
        == resources.files(ch_api_client.tests.fixtures)
        .joinpath("document.pdf")
        .read_bytes()
    )
