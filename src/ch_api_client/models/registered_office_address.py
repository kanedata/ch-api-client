import dataclasses
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import AddressBase, ItemLinkBase
from ch_api_client.models.enums import Country, ResponseKind


@dataclass
class LinksType(ItemLinkBase):
    pass


@dataclass
class RegisteredOfficeAddress(AddressBase):
    accept_appropriate_office_address_statement: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Setting this to true confirms that the new registered office address is an appropriate address as outlined in section 86(2) of the Companies Act 2006."
        },
    )
    country: Country | None = dataclasses.field(
        default=None,
        metadata={"description": "The country."},
    )
    premises: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The property name or number."},
    )
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the resource."},
    )
    kind: Literal[ResponseKind.REGISTERED_OFFICE_ADDRESS] | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of resource."},
    )
    links: LinksType | None = dataclasses.field(
        default=None,
        metadata={"description": "Links related to the registered office address."},
    )
