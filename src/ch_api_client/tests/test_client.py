import pytest
from pytest_httpx2 import HTTPXMock

from ch_api_client.client import CompaniesHouseAPI
from ch_api_client.tests.conftest import DUMMY_API_KEY, METHODS, MethodToTest


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

    document = client.get_document(
        doc_metadata.document_id,
        document_metadata=doc_metadata,
    )
    assert document is not None
    assert isinstance(document, bytes)
