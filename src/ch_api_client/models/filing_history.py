import dataclasses
import datetime as dt
from enum import StrEnum
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import CompanyNumber, ParametersBase
from ch_api_client.models.enums import ResponseKind


class FilingHistoryCategory(StrEnum):
    ACCOUNTS = "accounts"
    ADDRESS = "address"
    ANNUAL_RETURN = "annual-return"
    CAPITAL = "capital"
    CHANGE_OF_NAME = "change-of-name"
    INCORPORATION = "incorporation"
    LIQUIDATION = "liquidation"
    MISCELLANEOUS = "miscellaneous"
    MORTGAGE = "mortgage"
    OFFICERS = "officers"
    RESOLUTION = "resolution"
    CONFIRMATION_STATEMENT = "confirmation-statement"
    GAZETTE = "gazette"
    CHANGE = "change"
    DISSOLUTION = "dissolution"
    TERMINATION = "termination"
    APPOINTMENTS = "appointments"


@dataclass
class DescriptionValues:
    officer_name: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The name of the officer associated with the filing."},
    )
    termination_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The termination date of the officer associated with the filing."
        },
    )
    appointment_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The appointment date of the officer associated with the filing."
        },
    )
    made_up_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The made up date of the filing."},
    )
    change_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The change date of the filing."},
    )
    old_address: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The old address of the officer associated with the filing."
        },
    )
    new_address: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The new address of the officer associated with the filing."
        },
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The description of the filing."},
    )


@dataclass
class FilingHistoryListParameters(ParametersBase):
    category: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "One or more comma-separated categories to filter by (inclusive)."
        },
    )
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of filing history items to return per page."
        },
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The index into the entire result set that this result page starts."
        },
    )


@dataclass
class Annotation:
    annotation: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The annotation text."},
    )
    date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the annotation was added."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A description of the annotation.\n For enumeration descriptions see `description` section in the [enumeration mappings](https://github.com/companieshouse/api-enumerations/blob/master/filing_history_descriptions.yml) file."
        },
    )


@dataclass
class AssociatedFiling:
    date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the associated filing was processed."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A description of the associated filing.\n For enumeration descriptions see `description` section in the [enumeration mappings](https://github.com/companieshouse/api-enumerations/blob/master/filing_history_descriptions.yml) file."
        },
    )
    type: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of the associated filing."},
    )


@dataclass
class FilingHistoryItemLinks:
    self: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Link to this filing history item."},
    )
    document_metadata: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Link to the document metadata associated with this filing history item. See the Document API documentation for more details."
        },
    )


@dataclass
class Resolution:
    category: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The category of the resolution filed."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A description of the associated filing.\n For enumeration descriptions see `description` section in the [enumeration mappings] (https://github.com/companieshouse/api-enumerations/blob/master/filing_history_descriptions.yml) file."
        },
    )
    description_values: DescriptionValues | None = dataclasses.field(
        default=None,
        metadata={"description": "The description values associated with the filing."},
    )
    document_id: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The document id of the resolution."},
    )
    receive_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the resolution was processed."},
    )
    subcategory: Literal[FilingHistoryCategory.RESOLUTION] | None = dataclasses.field(
        default=None,
        metadata={"description": "The subcategory of the resolution filed."},
    )
    type: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of the associated filing."},
    )


@dataclass
class FilingHistoryItem:
    annotations: list[Annotation] | None = dataclasses.field(
        default_factory=list,
        metadata={"description": "Annotations for the filing"},
    )
    associated_filings: list[AssociatedFiling] | None = dataclasses.field(
        default_factory=list,
        metadata={"description": "Any filings associated with the current item"},
    )
    barcode: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The barcode of the document."},
    )
    transaction_id: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The transaction ID of the filing."},
    )
    category: FilingHistoryCategory | None = dataclasses.field(
        default=None,
        metadata={"description": "The category of the document filed."},
    )
    date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the filing was processed."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A description of the filing.\n For enumeration descriptions see `description` section in the [enumeration mappings](https://github.com/companieshouse/api-enumerations/blob/master/filing_history_descriptions.yml) file."
        },
    )
    description_values: DescriptionValues | None = dataclasses.field(
        default=None,
        metadata={"description": "The description values for the filing."},
    )
    links: FilingHistoryItemLinks | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Links to other resources associated with this filing history item."
        },
    )
    pages: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Number of pages within the PDF document (links.document_metadata)"
        },
    )
    paper_filed: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "If true, indicates this is a paper filing."},
    )
    resolutions: list[Resolution] | None = dataclasses.field(
        default_factory=list,
        metadata={"description": "Resolutions for the filing"},
    )
    subcategory: FilingHistoryCategory | None = dataclasses.field(
        default=None,
        metadata={"description": "The sub-category of the document filed."},
    )
    type: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of filing."},
    )

    @property
    def document_id(self) -> str | None:
        if self.links and self.links.document_metadata:
            return self.links.document_metadata.split("/")[-1]
        return None


@dataclass
class FilingHistoryList:
    filing_history_status: Literal["filing-history-available"] | None = (
        dataclasses.field(
            default=None,
            metadata={"description": "The status of the filing history."},
        )
    )
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the resource."},
    )
    items: list[FilingHistoryItem] | None = dataclasses.field(
        default_factory=list,
        metadata={"description": "The filing history items."},
    )
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of filing history items returned per page."
        },
    )
    kind: Literal[ResponseKind.FILING_HISTORY] | None = dataclasses.field(
        default=None,
        metadata={"description": "Indicates this resource is a filing history."},
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The index into the entire result set that this result page starts."
        },
    )
    total_count: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The total number of filing history items for this company."
        },
    )


@dataclass
class AnnualAccount:
    company_number: CompanyNumber = dataclasses.field(
        metadata={"description": "The company number of the annual account."},
    )
    financial_year_end: dt.date = dataclasses.field(
        metadata={"description": "The financial year end date of the annual account."},
    )
    document_id: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The document ID of the annual account."},
    )
    type: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of the annual account."},
    )
    has_ixbrl: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Indicates whether the annual account has iXBRL."},
    )
    has_pdf: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Indicates whether the annual account has a PDF version."
        },
    )


@dataclass
class AnnualAccountList:
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the resource."},
    )
    items: list[AnnualAccount] | None = dataclasses.field(
        default_factory=list,
        metadata={"description": "The annual account items."},
    )
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of annual account items returned per page."
        },
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The index into the entire result set that this result page starts."
        },
    )
    total_count: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The total number of annual account items for this company."
        },
    )
