import inspect
import typing
from dataclasses import InitVar, field
from types import UnionType

import click
from dotenv import load_dotenv
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from ch_api_client.client import CompaniesHouseAPI
from ch_api_client.models.document import ContentType

load_dotenv()


@dataclass
class CliContextObject:
    api_key: InitVar[str]
    pretty_print: bool = False
    client: CompaniesHouseAPI = field(init=False)

    def __post_init__(self, api_key: str):
        self.client = CompaniesHouseAPI(api_key)

    def to_json(self, result):
        result_adapter = TypeAdapter(type(result))
        indent = 4 if self.pretty_print else None
        return result_adapter.dump_json(result, indent=indent)


pass_client = click.make_pass_decorator(CliContextObject, ensure=True)


class ApiGroup(click.Group):
    def __init__(self, name=None, client=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self._client = client
        self._register: dict[str, str] = {}
        for attr_name in dir(self._client):
            attr = getattr(self._client, attr_name)
            if callable(attr) and getattr(attr, "_is_cli_method", False):
                command_name = attr_name.replace("_", "-")
                self._register[command_name] = attr_name

    def _get_base_type(self, annotation: typing.Any) -> typing.Any:
        if typing.get_origin(annotation) == UnionType:
            args = typing.get_args(annotation)
            args = [arg for arg in args if arg is not type(None)]
            if len(args) == 1:
                return args[0]
            raise ValueError(f"Cannot determine base type for annotation: {annotation}")
        return annotation

    def _param_to_param(
        self, param_name: str, param: inspect.Parameter
    ) -> click.Parameter:
        param_type = self._get_base_type(param.annotation)
        if param.default is inspect.Parameter.empty:
            return click.Argument([param_name.replace("_", "-")], type=param_type)
        else:
            return click.Option(
                [f"--{param_name.replace('_', '-')}"],
                type=param_type,
                default=param.default,
            )

    def list_commands(self, ctx):
        commands = super().list_commands(ctx)
        commands.extend(self._register.keys())
        return commands

    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd is not None:
            return cmd
        if cmd_name not in self._register:
            return None
        attr_name = self._register[cmd_name]
        attr = getattr(self._client, attr_name)
        params = []
        for param_name, param in inspect.signature(attr).parameters.items():
            if param_name == "self":
                continue
            params.append(self._param_to_param(param_name, param))

        @pass_client
        def func(obj: CliContextObject, *args, **kwargs):
            result = attr(obj.client, *args, **kwargs)
            if hasattr(result, "items"):
                items = result.items
                for item in items:
                    click.echo(obj.to_json(item))
            else:
                click.echo(obj.to_json(result))
            return result

        return click.Command(cmd_name, callback=func, help=attr.__doc__, params=params)


@click.group(cls=ApiGroup, client=CompaniesHouseAPI)
@click.option(
    "--api-key",
    help="Your Companies House API key.",
    envvar="CH_API_KEY",
)
@click.option(
    "--pretty-print/--no-pretty-print",
    default=False,
    help="Enable or disable pretty printing of JSON output.",
)
@click.pass_context
def cli(ctx: click.Context, api_key: str, pretty_print: bool):
    ctx.obj = CliContextObject(api_key=api_key, pretty_print=pretty_print)


@cli.command("get-filing-history-document")
@click.argument("company-number")
@click.argument("transaction-id")
@click.argument("output-file", type=click.File(mode="wb"), default="-")
@click.option(
    "--content-type",
    type=ContentType,
)
@pass_client
def get_filing_history_document(
    obj: CliContextObject,
    company_number: str,
    transaction_id: str,
    output_file: click.File,
    content_type: ContentType | None = None,
):
    client = obj.client
    document_metadata = client.get_document_metadata(company_number, transaction_id)
    result = client.get_document(document_metadata, content_type=content_type)
    output_file.write(result)  # type: ignore
