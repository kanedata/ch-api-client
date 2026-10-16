import dataclasses
import datetime as dt

from pydantic.dataclasses import dataclass


class CompanyNumber(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return handler(str)


class SICCode(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return handler(str)


@dataclass
class ParametersBase:
    pass


@dataclass
class LinkBase:
    pass


@dataclass
class ItemLinkBase(LinkBase):
    self: str = dataclasses.field(metadata={"description": "URL to this resource."})


@dataclass
class AddressBase:
    address_line_1: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The first line of the address."},
    )
    address_line_2: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The second line of the address."},
    )
    locality: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The locality e.g London."},
    )
    po_box: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The post-office box number."},
    )
    postal_code: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The postal code e.g CF14 3UZ."},
    )
    care_of: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The care of name."},
    )
    region: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The region e.g Surrey."},
    )


@dataclass
class DateOfBirthBase:
    month: int = dataclasses.field()
    year: int = dataclasses.field()


@dataclass
class AccountingDateBase:
    day: int = dataclasses.field()
    month: int = dataclasses.field()

    def to_dt(self, year: int) -> dt.date:
        return dt.date(year=year, month=self.month, day=self.day)
