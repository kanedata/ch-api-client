import dataclasses

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import AddressBase, DateOfBirthBase


@dataclass
class OfficerDateOfBirth(DateOfBirthBase):
    month: int = dataclasses.field(
        metadata={"description": "The month the officer was born in."},
    )
    year: int = dataclasses.field(
        metadata={"description": "The year the officer was born in."},
    )


@dataclass
class OfficerAddress(AddressBase):
    country: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The country."},
    )
    premises: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The property name or number."},
    )
