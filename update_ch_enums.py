from pathlib import Path
from textwrap import dedent

import chardet
import click
import httpx2
import yaml

CONSTANTS_URLS = [
    "https://raw.githubusercontent.com/companieshouse/api-enumerations/refs/heads/master/constants.yml",
    "https://raw.githubusercontent.com/companieshouse/api-enumerations/refs/heads/master/mortgage_descriptions.yml",
    "https://raw.githubusercontent.com/companieshouse/api-enumerations/refs/heads/master/psc_descriptions.yml",
]
OUTPUT_PATH = Path(__file__).parent / "src" / "ch_api_client" / "models" / "ch_enums.py"


def snake_to_camel(snake_str):
    components = snake_str.replace("-", "_").split("_")
    return components[0].title() + "".join(x.title() for x in components[1:])


def get_value_key(value):
    value_key = str(value).upper().replace("-", "_")
    if value_key[0].isdigit():
        value_key = "_" + value_key
    return value_key


FILE_TEMPLATE = """
    # ruff: noqa
    # fmt: off
    from enum import StrEnum
"""


@click.command()
@click.option(
    "--constants-url",
    default=CONSTANTS_URLS,
    help="URL to fetch the constants YAML from.",
    multiple=True,
)
@click.option(
    "--output-path", default=OUTPUT_PATH, help="Path to save the generated enums."
)
def update_ch_enums(constants_url, output_path):
    constants = {}
    for url in constants_url:
        response = httpx2.get(url)
        response_encoding = chardet.detect(response.content, max_bytes=10000)[
            "encoding"
        ]
        if response_encoding is None:
            response_encoding = "utf-8"
        constants.update(yaml.safe_load(response.content.decode(response_encoding)))
    with open(output_path, "w") as f:
        f.write(dedent(FILE_TEMPLATE).strip())
        for key, values in constants.items():
            print(key)
            values = {str(k): str(v) for k, v in values.items()}
            f.write("\n\n")
            f.write(f"class {snake_to_camel(key)}(StrEnum):\n")
            f.writelines(
                f"    {get_value_key(value)} = '{value}'  # {description}\n"
                for value, description in values.items()
            )
        f.write("\n\n")


if __name__ == "__main__":
    update_ch_enums()
