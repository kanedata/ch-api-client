import dataclasses
import datetime as dt
from enum import StrEnum

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import AddressBase, LinkBase
from ch_api_client.models.ch_enums import InsolvencyCaseDateType, InsolvencyCaseType


class PractitionerRole(StrEnum):
    FINAL_LIQUIDATOR = "final-liquidator"
    RECEIVER = "receiver"
    RECEIVER_MANAGER = "receiver-manager"
    PROPOSED_LIQUIDATOR = "proposed-liquidator"
    PROVISIONAL_LIQUIDATOR = "provisional-liquidator"
    ADMINISTRATIVE_RECEIVER = "administrative-receiver"
    PRACTITIONER = "practitioner"
    INTERIM_LIQUIDATOR = "interim-liquidator"


@dataclass
class CaseDates:
    type: InsolvencyCaseDateType | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Describes what date is represented by the associated `date` element."
        },
    )
    date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The case date, described by `date_type`."},
    )


@dataclass
class PractitionerAddress(AddressBase):
    country: str | None = dataclasses.field(
        default=None, metadata={"description": "The country."}
    )


@dataclass
class Links(LinkBase):
    charge: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The link to the charge this case is lodged against."},
    )


@dataclass
class Practitioner:
    name: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The name of the practitioner."},
    )
    address: PractitionerAddress | None = dataclasses.field(
        default=None,
        metadata={"description": "The practitioners' address."},
    )
    appointed_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the practitioner was appointed on."},
    )
    ceased_to_act_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the practitioner ceased to act for the case."
        },
    )
    role: PractitionerRole | None = dataclasses.field(
        default=None,
        metadata={"description": "The role of the practitioner in the case."},
    )


@dataclass
class Case:
    type: InsolvencyCaseType | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of case."},
    )
    dates: list[CaseDates] | None = dataclasses.field(
        default=None,
        metadata={"description": "The dates specific to the case."},
    )
    notes: list[str] | None = dataclasses.field(
        default=None,
        metadata={"description": "Additional notes related to the insolvency case."},
    )
    practitioners: list[Practitioner] | None = dataclasses.field(
        default=None,
        metadata={"description": "The practitioners for the case."},
    )
    links: Links | None = dataclasses.field(
        default=None,
        metadata={"description": "The links for the case."},
    )
    number: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The case number."},
    )


@dataclass
class CompanyInsolvency:
    cases: list[Case] = dataclasses.field(
        default_factory=list,
        metadata={"description": "List of insolvency cases."},
    )
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the resource."},
    )
    status: list[InsolvencyCaseType] | None = dataclasses.field(
        default=None,
        metadata={"description": "Company insolvency status details"},
    )
