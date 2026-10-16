import json
from importlib import resources

import pytest
from click.testing import CliRunner
from pytest_httpx2 import HTTPXMock

import ch_api_client.tests.fixtures
from ch_api_client.cli import cli
from ch_api_client.tests.conftest import DUMMY_API_KEY, METHODS, MethodToTest


@pytest.mark.parametrize("method", METHODS, ids=str)
def test_ch_api_cli(httpx2_mock: HTTPXMock, method: MethodToTest):
    method.add_url_mocks(httpx2_mock)
    runner = CliRunner()
    result = method.invoke_command(runner)
    if result.exit_code != 0:
        print(result.output)
    assert result.exit_code == 0
    split_result = result.output.splitlines()
    for line in split_result:
        assert line is not None
        assert json.loads(line) is not None


def test_ch_api_cli_get_document(doc_mock: HTTPXMock):
    method = next(m for m in METHODS if m.method_name == "get_filing_history")
    method.add_url_mocks(doc_mock)
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
