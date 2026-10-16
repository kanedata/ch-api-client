import dataclasses
import datetime as dt
from enum import StrEnum

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import (
    AddressBase,
    DateOfBirthBase,
    LinkBase,
    ParametersBase,
)
from ch_api_client.models.ch_enums import SuperSecureDescription


class PscKind(StrEnum):
    INDIVIDUAL_PERSON_WITH_SIGNIFICANT_CONTROL = (
        "individual-person-with-significant-control"
    )
    CORPORATE_ENTITY_PERSON_WITH_SIGNIFICANT_CONTROL = (
        "corporate-entity-person-with-significant-control"
    )
    LEGAL_PERSON_WITH_SIGNIFICANT_CONTROL = "legal-person-with-significant-control"
    SUPER_SECURE_PERSON_WITH_SIGNIFICANT_CONTROL = (
        "super-secure-person-with-significant-control"
    )
    INDIVIDUAL_BENEFICIAL_OWNER = "individual-beneficial-owner"
    CORPORATE_ENTITY_BENEFICIAL_OWNER = "corporate-entity-beneficial-owner"
    LEGAL_PERSON_BENEFICIAL_OWNER = "legal-person-beneficial-owner"
    SUPER_SECURE_BENEFICIAL_OWNER = "super-secure-beneficial-owner"


@dataclass
class CompanyPSCListParameters(ParametersBase):
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={"description": "The number of items to return per page."},
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The index into the entire result set that this result page starts."
        },
    )
    register_view: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Display register specific information."},
    )


@dataclass
class DateOfBirthPSCList(DateOfBirthBase):
    pass


@dataclass
class NameElements:
    forename: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The forename of the person with significant control."
        },
    )
    middle_name: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The middle name of the person with significant control."
        },
    )
    surname: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The surname of the person with significant control."},
    )
    title: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Title of the person with significant control."},
    )


@dataclass
class PscItemsListLinksPSC(LinkBase):
    notifications: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Link to the persons with significant control notification resource that this notification is associated with."
        },
    )


@dataclass
class PscItemsListLinksType(LinkBase):
    self: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The URL of the resource."},
    )
    statement: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The URL of the statement linked to this person with significant control.",
        },
    )
    persons_with_significant_control: PscItemsListLinksPSC | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Links to other persons with significant control resources associated with this person with significant control list item."
        },
    )


@dataclass
class PscListIdent:
    legal_authority: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The legal authority supervising the corporate entity or legal person with significant control."
        },
    )
    legal_form: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The legal form of the corporate entity or legal person with significant control as defined by its country of registration."
        },
    )
    place_registered: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The place the corporate entity with significant control is registered."
        },
    )
    registration_number: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The registration number of the corporate entity with significant control."
        },
    )
    country_registered: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The country or state the corporate entity with significant control is registered in."
        },
    )


@dataclass
class IdentityVerificationDetails:
    anti_money_laundering_supervisory_bodies: list[str] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The Anti-Money Laundering supervisory bodies that the authorised corporate service provider was registered with when verifying the person with significant control."
        },
    )
    appointment_verification_end_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date on which the identity verification statement was removed for the notification."
        },
    )
    appointment_verification_statement_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date from which an identity verification statement can be supplied for the notification."
        },
    )
    appointment_verification_statement_due_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date by which an identity verification statement must be supplied for the notification."
        },
    )
    appointment_verification_start_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date on which the identity verification statement was supplied for the notification."
        },
    )
    authorised_corporate_service_provider_name: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The name of the authorised corporate service provider that verified the identity of the person with significant control."
        },
    )
    identity_verified_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date on which the authorised corporate service provider verified the identity of the person with significant control."
        },
    )
    preferred_name: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The name provided to the authorised corporate service provider by which the person with significant control prefers to be known."
        },
    )


@dataclass
class PscAddress(AddressBase):
    country: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The country. For example, UK."},
    )
    premises: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The property name or number."},
    )


@dataclass
class BeneficialOwnerAddress(PscAddress):
    pass


@dataclass
class PscListLinksType(LinkBase):
    self: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The link to the current PSC list."},
    )
    persons_with_significant_control_list: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The link to the list of persons with significant control."
        },
    )


@dataclass
class ListSummary:
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The entity tag for the list summary."},
    )
    notified_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date on which the list summary was notified."},
    )
    ceased_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date on which the list summary was ceased."},
    )
    country_of_residence: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The country of residence for the list summary."},
    )
    date_of_birth: DateOfBirthPSCList | None = dataclasses.field(
        default=None,
        metadata={"description": "The date of birth for the list summary."},
    )
    name: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The name for the list summary."},
    )
    name_elements: NameElements | None = dataclasses.field(
        default=None,
        metadata={"description": "The name elements for the list summary."},
    )
    links: PscItemsListLinksType | None = dataclasses.field(
        default=None,
        metadata={"description": "The links for the list summary."},
    )
    nationality: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The nationality for the list summary."},
    )
    identification: PscListIdent | None = dataclasses.field(
        default=None,
        metadata={"description": "The identification details for the list summary."},
    )
    identity_verification_details: IdentityVerificationDetails | None = (
        dataclasses.field(
            default=None,
            metadata={
                "description": "The identity verification details for the list summary."
            },
        )
    )
    ceased: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Indicates whether the list summary has ceased."},
    )
    description: SuperSecureDescription | None = dataclasses.field(
        default=None,
        metadata={"description": "The description for the list summary."},
    )
    kind: PscKind | None = dataclasses.field(default=None)
    address: PscAddress | None = dataclasses.field(
        default=None,
        metadata={"description": "The address for the list summary."},
    )
    natures_of_control: list[str] | None = dataclasses.field(
        default=None,
        metadata={"description": "The natures of control for the list summary."},
    )
    is_sanctioned: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Indicates whether the list summary is sanctioned."},
    )
    principal_office_address: BeneficialOwnerAddress | None = dataclasses.field(
        default=None,
        metadata={"description": "The principal office address for the list summary."},
    )


@dataclass
class CompanyPSCList:
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of persons with significant control to return per page."
        },
    )
    items: list[ListSummary] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The list of persons with significant control."},
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The offset into the entire result set that this page starts.",
        },
    )
    total_results: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The total number of persons with significant control in this result set.",
        },
    )
    active_count: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of active persons with significant control in this result set.",
        },
    )
    ceased_count: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of ceased persons with significant control in this result set.",
        },
    )
    links: PscListLinksType | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A set of URLs related to the resource, including self.",
        },
    )
