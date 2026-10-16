import dataclasses
import datetime as dt

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import LinkBase, ParametersBase
from ch_api_client.models.ch_enums import (
    AssetsCeasedReleased,
    Classificationdesc,
    ParticularDescription,
    SecuredDetailsDescription,
    Status,
)


@dataclass
class ChargesParameters(ParametersBase):
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={"description": "The number of charges to return per page."},
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The index into the entire result set that this result page starts."
        },
    )


@dataclass
class AlterationsDesc:
    has_alterations_to_order: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "The charge has alterations to order"},
    )
    has_alterations_to_prohibitions: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "The charge has alterations to prohibitions"},
    )
    has_alterations_to_provisions: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "The charge has alterations to provisions"},
    )


@dataclass
class SecuredDetailsDesc:
    type: SecuredDetailsDescription | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of secured details."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Details of the amount or obligation secured by the charge"
        },
    )


@dataclass
class ParticularDesc:
    type: ParticularDescription | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of secured details."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Details of the amount or obligation secured by the charge"
        },
    )
    contains_floating_charge: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "The charge contains a floating charge"},
    )
    contains_fixed_charge: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "The charge contains a fixed charge"},
    )
    floating_charge_covers_all: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The floating charge covers all the property or undertaking or the company"
        },
    )
    contains_negative_pledge: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "The charge contains a negative pledge"},
    )
    charger_acting_as_bare_trustee: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The chargor is acting as a bare trustee for the property"
        },
    )


@dataclass
class ClassificationDesc:
    type: Classificationdesc | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of charge classication."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Details of the charge classification"},
    )


@dataclass
class PersonsEntitled:
    name: str = dataclasses.field(
        metadata={"description": "The name of the person entitled."},
    )


@dataclass
class TransactionLinks(LinkBase):
    filing: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Link to the charge filing data"},
    )
    insolvency_case: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Link to the insolvency case related to this filing"},
    )


@dataclass
class Transactions:
    filing_type: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Filing type which created, updated or satisfied the charge"
        },
    )
    delivered_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the filing was submitted to Companies House"
        },
    )
    insolvency_case_number: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The insolvency case related to this filing"},
    )
    links: TransactionLinks | None = dataclasses.field(
        default=None,
        metadata={"description": "The resources related to this filing"},
    )


@dataclass
class InsolvencyCaseLinks(LinkBase):
    case: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Link to the insolvency case data"},
    )


@dataclass
class InsolvencyCases:
    case_number: str = dataclasses.field(
        metadata={"description": "The number of this insolvency case"}
    )
    links: InsolvencyCaseLinks | None = dataclasses.field(
        default=None,
        metadata={"description": "The resources related to this insolvency case"},
    )


@dataclass
class ChargeLinks(LinkBase):
    self: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Link to the this charge data"},
    )


@dataclass
class ChargeDetails:
    etag: str = dataclasses.field()
    charge_number: int = dataclasses.field(
        metadata={
            "description": "The charge number is used to reference an individual charge"
        }
    )
    status: Status = dataclasses.field(
        metadata={"description": "The status of the charge"}
    )
    classification: list[ClassificationDesc] | ClassificationDesc = dataclasses.field(
        metadata={"description": "Classification information"}
    )
    id: str | None = dataclasses.field(
        default=None, metadata={"description": "The id of the charge"}
    )
    charge_code: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The charge code is a replacement of the mortgage description"
        },
    )
    assests_ceased_released: AssetsCeasedReleased | None = dataclasses.field(
        default=None,
        metadata={"description": "Cease/release information about the charge."},
    )
    acquired_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the property or undertaking was acquired on"
        },
    )
    delivered_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the charge was submitted to Companies House"
        },
    )
    resolved_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the issue was resolved on"},
    )
    covering_instrument_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date by which the series of debentures were created"
        },
    )
    created_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the charge was created"},
    )
    satisfied_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the charge was satisfied"},
    )
    particulars: list[ParticularDesc] | ParticularDesc | None = dataclasses.field(
        default=None,
        metadata={"description": "Details of charge or undertaking"},
    )
    secured_details: list[SecuredDetailsDesc] | SecuredDetailsDesc | None = (
        dataclasses.field(
            default=None,
            metadata={
                "description": "Information about what is secured against this charge"
            },
        )
    )
    scottish_alterations: list[AlterationsDesc] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Information about alterations for Scottish companies"
        },
    )
    more_than_four_persons_entitled: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Charge has more than four person entitled"},
    )
    persons_entitled: list[PersonsEntitled] | None = dataclasses.field(
        default=None,
        metadata={"description": "People that are entitled to the charge"},
    )
    transactions: list[Transactions] | None = dataclasses.field(
        default=None,
        metadata={"description": "Transactions that have been filed for the charge."},
    )
    insolvency_cases: list[InsolvencyCases] | None = dataclasses.field(
        default=None,
        metadata={"description": "Details of any insolvency related to the charge"},
    )
    links: ChargeLinks | None = dataclasses.field(
        default=None,
        metadata={"description": "The resources related to this charge"},
    )


@dataclass
class ChargeList:
    etag: str = dataclasses.field(metadata={"description": "The ETag of the resource."})
    items: list[ChargeDetails] = dataclasses.field(
        metadata={"description": "List of charges"}
    )
    total_count: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Total number of charges returned by the API (filtering applies)."
        },
    )
    unfiletered_count: int | None = dataclasses.field(
        default=None,
        metadata={"description": "The total number of unfiltered charges."},
    )
    satisfied_count: int | None = dataclasses.field(
        default=None,
        metadata={"description": "Number of satisfied charges"},
    )
    part_satisfied_count: int | None = dataclasses.field(
        default=None,
        metadata={"description": "Number of part satisfied charges"},
    )

    @property
    def unfiltered_count(self) -> int | None:
        return self.unfiletered_count
