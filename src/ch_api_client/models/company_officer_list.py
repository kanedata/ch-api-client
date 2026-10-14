import dataclasses
import datetime as dt
from enum import StrEnum
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import ParametersBase
from ch_api_client.models._shared import OfficerAddress, OfficerDateOfBirth
from ch_api_client.models.ch_enums import IdentificationType, OfficerRole
from ch_api_client.models.enums import ResponseKind


class RegisterType(StrEnum):
    DIRECTORS = "directors"
    SECRETARIES = "secretaries"
    LLP_MEMBERS = "llp_members"


class RegisterView(StrEnum):
    TRUE = "true"
    FALSE = "false"


class OrderBy(StrEnum):
    APPOINTED_ON = "appointed_on"
    RESIGNED_ON = "resigned_on"
    SURNAME = "surname"


@dataclass
class CompanyOfficerListParameters(ParametersBase):
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of items to return per page for the officer list."
        },
    )
    register_type: RegisterType | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The register_type determines which officer type is returned for the registers view.The register_type field will only work if registers_view is set to true"
        },
    )
    register_view: RegisterView | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Display register specific information. If given register is held at Companies House, registers_view set to true and correct register_type specified, only active officers will be returned. Defaults to false"
        },
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The offset into the entire result set that this page starts."
        },
    )
    order_by: OrderBy | None = dataclasses.field(
        default=None,
        metadata={"description": "The field by which to order the result set."},
    )


@dataclass
class OfficerLinkTypes:
    appointments: str = dataclasses.field(
        metadata={
            "description": "Link to the officer appointment resource that this appointment is associated with."
        }
    )


@dataclass
class ItemLinkTypes:
    self: str = dataclasses.field(
        metadata={
            "description": "Link to this individual company officer appointment resource."
        }
    )
    officer: OfficerLinkTypes = dataclasses.field(
        metadata={
            "description": "Links to other officer resources associated with this officer list item."
        }
    )


@dataclass
class FormerNames:
    forenames: str = dataclasses.field(
        metadata={"description": "Former forenames of the officer."}
    )
    surname: str = dataclasses.field(
        metadata={"description": "Former surnames of the officer."}
    )


@dataclass
class IdentityVerificationDetails:
    anti_money_laundering_supervisory_bodies: list[str] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The Anti-Money Laundering supervisory bodies that the authorised corporate service provider was registered with when verifying the officer."
        },
    )
    appointment_verification_end_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date on which the identity verification statement was removed for the appointment."
        },
    )
    appointment_verification_statement_due_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date by which an identity verification statement must be supplied for the appointment."
        },
    )
    appointment_verification_start_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date on which the identity verification statement was supplied for the appointment."
        },
    )
    authorised_corporate_service_provider_name: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The name of the authorised corporate service provider that verified the identity of the officer."
        },
    )
    identity_verified_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date on which the authorised corporate service provider verified the identity of the officer."
        },
    )
    preferred_name: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The name provided to the authorised corporate service provider by which the officer prefers to be known."
        },
    )


@dataclass
class CorporateIdent:
    identification_type: IdentificationType | None = dataclasses.field(
        default=None, metadata={"description": "The officer's identity type"}
    )
    legal_authority: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The legal authority supervising the company."},
    )
    legal_form: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The legal form of the company as defined by its country of registration."
        },
    )
    place_registered: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Place registered."},
    )
    registration_number: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Company registration number."},
    )


@dataclass
class ContactDetails:
    contact_name: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The name of the contact."},
    )


@dataclass
class OfficerSummary:
    address: OfficerAddress | None = dataclasses.field(
        default=None,
        metadata={"description": "The correspondence address of the officer."},
    )
    appointed_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date on which the officer was appointed. For the officer roles of `corporate-managing-officer` and `managing-officer` this is the date on which Companies House was notified about the officer."
        },
    )
    contact_details: ContactDetails | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The contact at the `corporate-managing-officer` of a `registered-overseas-entity`."
        },
    )
    country_of_residence: str | None = dataclasses.field(
        default=None, metadata={"description": "The officer's place of residence."}
    )
    date_of_birth: OfficerDateOfBirth | None = dataclasses.field(
        default=None, metadata={"description": "Details of director date of birth."}
    )
    links: ItemLinkTypes | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Links to other resources associated with this officer list item."
        },
    )
    name: str | None = dataclasses.field(
        default=None, metadata={"description": "Corporate or natural officer name."}
    )
    nationality: str | None = dataclasses.field(
        default=None, metadata={"description": "The officer's nationality."}
    )
    occupation: str | None = dataclasses.field(
        default=None, metadata={"description": "The officer's job title."}
    )
    officer_role: OfficerRole | None = dataclasses.field(
        default=None,
    )
    person_number: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Unique person identifier as displayed in bulk products 195, 198, 208, 209 and 216."
        },
    )
    principal_office_address: OfficerAddress | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The principal/registered office address of a `corporate-managing-officer` of a `registered-overseas-entity`."
        },
    )
    resigned_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the officer was resigned. For the officer roles of `corporate-managing-officer` and `managing-officer` this is the date on which Companies House was notified about the officers cessation."
        },
    )
    responsibilities: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The responsibilities of the managing officer of a `registered-overseas-entity`."
        },
    )
    former_names: list[FormerNames] | None = dataclasses.field(
        default=None, metadata={"description": "Former names for the officer."}
    )
    identification: CorporateIdent | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Only one from `eea`, `non-eea`, `uk-limited-company`, `other-corporate-body-or-firm` or `registered-overseas-entity-corporate-managing-officer` can be supplied, not multiples of them."
        },
    )
    identity_verification_details: IdentityVerificationDetails | None = (
        dataclasses.field(
            default=None,
            metadata={
                "description": "Information relating to the identity verification of the officer"
            },
        )
    )
    appointed_before: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the officer was appointed before. Only present when the <code>is_pre_1992_appointment</code> attribute is <code>true</code>."
        },
    )
    etag: str | None = dataclasses.field(
        default=None, metadata={"description": "The Etag of the resource"}
    )
    is_pre_1992_appointment: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Indicator representing if the officer was appointed before their appointment date."
        },
    )


@dataclass
class LinkTypes:
    self: str = dataclasses.field(
        metadata={"description": "Link to this officer list resource."}
    )


@dataclass
class OfficerList:
    active_count: int = dataclasses.field(
        metadata={"description": "The number of active officers in this result set."}
    )
    items: list[OfficerSummary] = dataclasses.field(
        metadata={"description": "The list of officer summaries in this result set."}
    )
    items_per_page: int = dataclasses.field(
        metadata={"description": "The number of items per page in this result set."},
    )
    links: LinkTypes = dataclasses.field(
        metadata={
            "description": "Links to other resources associated with this officer list resource."
        }
    )
    resigned_count: int = dataclasses.field(
        metadata={"description": "The number of resigned officers in this result set."}
    )
    start_index: int = dataclasses.field(
        metadata={
            "description": "The offset into the entire result set that this page starts."
        }
    )
    total_results: int = dataclasses.field(
        metadata={"description": "The total number of officers in this result set."}
    )
    kind: Literal[ResponseKind.OFFICER_LIST] = dataclasses.field(
        default=ResponseKind.OFFICER_LIST,
        metadata={"description": "The kind of the resource."},
    )
    etag: str | None = dataclasses.field(
        default=None, metadata={"description": "The ETag of the resource."}
    )
