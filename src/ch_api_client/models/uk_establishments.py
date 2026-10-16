import dataclasses
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import CompanyNumber, ItemLinkBase, LinkBase
from ch_api_client.models.enums import ResponseKind


@dataclass
class SelfLinks(ItemLinkBase):
    pass


@dataclass
class Links(LinkBase):
    company: str = dataclasses.field(
        metadata={"description": "The link to the company."},
    )


@dataclass
class CompanyDetails:
    company_number: CompanyNumber = dataclasses.field(
        metadata={"description": "The number of the company."},
    )
    company_name: str = dataclasses.field(
        metadata={"description": "The name of the company."},
    )
    company_status: str = dataclasses.field(
        metadata={"description": "Company status."},
    )
    locality: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The locality e.g London."},
    )
    links: Links | None = dataclasses.field(
        default=None,
        metadata={"description": "Resources related to this company."},
    )


@dataclass
class CompanyUKEstablishments:
    etag: str | None = dataclasses.field(
        default=None, metadata={"description": "The ETag of the resource."}
    )
    kind: (
        Literal[ResponseKind.UKESTABLISHMENT_COMPANIES, ResponseKind.RELATED_COMPANIES]
        | None
    ) = dataclasses.field(default=None)
    links: SelfLinks | None = dataclasses.field(
        default=None,
        metadata={
            "description": "UK Establishment Resources related to this company.",
        },
    )
    items: list[CompanyDetails] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "List of UK Establishment companies.",
        },
    )
