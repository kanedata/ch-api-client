import dataclasses
import datetime as dt
from enum import StrEnum
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import ItemLinkBase
from ch_api_client.models.enums import ResponseKind


class ExemptionType(StrEnum):
    PSC_EXEMPT_AS_TRADING_ON_REGULATED_MARKET = (
        "psc-exempt-as-trading-on-regulated-market"
    )
    PSC_EXEMPT_AS_SHARES_ADMITTED_ON_MARKET = "psc-exempt-as-shares-admitted-on-market"
    PSC_EXEMPT_AS_TRADING_ON_UK_REGULATED_MARKET = (
        "psc-exempt-as-trading-on-uk-regulated-market"
    )
    PSC_EXEMPT_AS_TRADING_ON_EU_REGULATED_MARKET = (
        "psc-exempt-as-trading-on-eu-regulated-market"
    )
    DISCLOSURE_TRANSPARENCY_RULES_CHAPTER_FIVE_APPLIES = (
        "disclosure-transparency-rules-chapter-five-applies"
    )


@dataclass
class LinksType(ItemLinkBase):
    pass


@dataclass
class ExemptionItem:
    exempt_from: dt.date = dataclasses.field(
        metadata={"description": "Exemption valid from."}
    )
    exempt_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "Exemption valid to."},
    )


@dataclass
class ExemptionItemWrapper:
    exemption_type: ExemptionType = dataclasses.field(
        metadata={"description": "The type of exemption."},
    )
    items: list[ExemptionItem] = dataclasses.field(
        default_factory=list,
        metadata={"description": "List of dates"},
    )


@dataclass
class PscExemptAsTradingOnRegulatedMarketItem(ExemptionItemWrapper):
    pass


@dataclass
class PscExemptAsSharesAdmittedOnMarketItem(ExemptionItemWrapper):
    pass


@dataclass
class PscExemptAsTradingOnUkRegualatedMarketItem(ExemptionItemWrapper):
    pass


@dataclass
class PscExemptAsTradingOnEuRegualatedMarketItem(ExemptionItemWrapper):
    pass


@dataclass
class DiclosureTransparencyRulesChapterFiveAppliesItem(ExemptionItemWrapper):
    pass


@dataclass
class Exemptions:
    psc_exempt_as_trading_on_regulated_market: (
        PscExemptAsTradingOnRegulatedMarketItem | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "If present the company has been or is exempt from keeping a PSC register, as it has voting shares admitted to trading on a regulated market other than the UK.",
        },
    )
    psc_exempt_as_shares_admitted_on_market: (
        PscExemptAsSharesAdmittedOnMarketItem | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "If present the company has been or is exempt from keeping a PSC register, as it has voting shares admitted to trading on a market listed in the Register of People with Significant Control Regulations 2016.",
        },
    )
    psc_exempt_as_trading_on_uk_regulated_market: (
        PscExemptAsTradingOnUkRegualatedMarketItem | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "If present the company has been or is exempt from keeping a PSC register, as it has voting shares admitted to trading on a UK regulated market.",
        },
    )
    psc_exempt_as_trading_on_eu_regulated_market: (
        PscExemptAsTradingOnEuRegualatedMarketItem | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "If present the company has been or is exempt from keeping a PSC register, as it has voting shares admitted to trading on an EU regulated market.",
        },
    )
    disclosure_transparency_rules_chapter_five_applies: (
        DiclosureTransparencyRulesChapterFiveAppliesItem | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "If present the company has been or is exempt from keeping a PSC register, because it is a DTR issuer and the shares are admitted to trading on a regulated market.",
        },
    )


@dataclass
class CompanyExemptions:
    links: LinksType | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A set of URLs related to the resource, including self."
        },
    )
    kind: Literal[ResponseKind.EXEMPTIONS] = dataclasses.field(
        default=ResponseKind.EXEMPTIONS,
        metadata={"description": "The kind of the response."},
    )
    exemptions: Exemptions | None = dataclasses.field(
        default=None,
        metadata={"description": "Company exemptions information."},
    )
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the resource."},
    )
