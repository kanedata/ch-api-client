import dataclasses
import datetime as dt
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import CompanyNumber, ItemLinkBase, LinkBase
from ch_api_client.models.ch_enums import RegisterLocations, RegisterTypes
from ch_api_client.models.enums import ResponseKind


@dataclass
class LinksType(ItemLinkBase):
    pass


@dataclass
class LinksItems(LinkBase):
    filing: str = dataclasses.field(
        metadata={"description": "The URL of the transaction for the resource."}
    )


@dataclass
class LinksDirectorsRegister(LinkBase):
    directors_register: str = dataclasses.field(
        metadata={"description": "The URL for the resource."}
    )


@dataclass
class LinksSecretariesRegister(LinkBase):
    secretaries_register: str = dataclasses.field(
        metadata={"description": "The URL for the resource."}
    )


@dataclass
class LinksPersonsWithSignificantControlRegister(LinkBase):
    persons_with_significant_control_register: str = dataclasses.field(
        metadata={"description": "The URL for the resource."}
    )


@dataclass
class LinksListUsualResidentialAddress(LinkBase):
    usual_residential_address: str = dataclasses.field(
        metadata={"description": "The URL for the resource."}
    )


@dataclass
class LinksListLLPUsualResidentialAddress(LinkBase):
    llp_usual_residential_address: str = dataclasses.field(
        metadata={"description": "The URL for the resource."}
    )


@dataclass
class LinksListMembers(LinkBase):
    members: str = dataclasses.field(
        metadata={"description": "The URL for the resource."}
    )


@dataclass
class LinksListLLPMembers(LinkBase):
    llp_members: str = dataclasses.field(
        metadata={"description": "The URL for the resource."}
    )


@dataclass
class RegisteredItems:
    moved_on: dt.date = dataclasses.field(
        metadata={"description": "The date registered on"}
    )
    register_moved_to: RegisterLocations = dataclasses.field(
        metadata={"description": "Location of registration"}
    )
    links: LinksItems | None = dataclasses.field(
        default=None, metadata={"description": "Links related to the registered item."}
    )


@dataclass
class RegisterListBase:
    items: list[RegisteredItems]


@dataclass
class RegisterListDirectors(RegisterListBase):
    register_type: Literal[RegisterTypes.DIRECTORS] = dataclasses.field(
        default=RegisterTypes.DIRECTORS, metadata={"description": "The register type."}
    )
    links: LinksDirectorsRegister | None = dataclasses.field(
        default=None,
        metadata={"description": "A set of URLs related to the resource."},
    )


@dataclass
class RegisterListSecretaries(RegisterListBase):
    register_type: Literal[RegisterTypes.SECRETARIES] = dataclasses.field(
        default=RegisterTypes.SECRETARIES,
        metadata={"description": "The register type."},
    )
    links: LinksSecretariesRegister | None = dataclasses.field(
        default=None,
        metadata={"description": "A set of URLs related to the resource."},
    )


@dataclass
class RegisterListPersonsWithSignificantControl(RegisterListBase):
    register_type: Literal[RegisterTypes.PERSONS_WITH_SIGNIFICANT_CONTROL] = (
        dataclasses.field(
            default=RegisterTypes.PERSONS_WITH_SIGNIFICANT_CONTROL,
            metadata={"description": "The register type."},
        )
    )
    links: LinksPersonsWithSignificantControlRegister | None = dataclasses.field(
        default=None,
        metadata={"description": "A set of URLs related to the resource."},
    )


@dataclass
class RegisterListUsualResidentialAddress(RegisterListBase):
    register_type: Literal[RegisterTypes.USUAL_RESIDENTIAL_ADDRESS] = dataclasses.field(
        default=RegisterTypes.USUAL_RESIDENTIAL_ADDRESS,
        metadata={"description": "The register type."},
    )
    links: LinksListUsualResidentialAddress | None = dataclasses.field(
        default=None,
        metadata={"description": "A set of URLs related to the resource."},
    )


@dataclass
class RegisterListLLPUsualResidentialAddress(RegisterListBase):
    register_type: Literal[RegisterTypes.LLP_USUAL_RESIDENTIAL_ADDRESS] = (
        dataclasses.field(
            default=RegisterTypes.LLP_USUAL_RESIDENTIAL_ADDRESS,
            metadata={"description": "The register type."},
        )
    )
    links: LinksListLLPUsualResidentialAddress | None = dataclasses.field(
        default=None,
        metadata={"description": "A set of URLs related to the resource."},
    )


@dataclass
class RegisterListMembers(RegisterListBase):
    register_type: Literal[RegisterTypes.MEMBERS] = dataclasses.field(
        default=RegisterTypes.MEMBERS, metadata={"description": "The register type."}
    )
    links: LinksListMembers | None = dataclasses.field(
        default=None,
        metadata={"description": "A set of URLs related to the resource."},
    )


@dataclass
class RegisterListLLPMembers(RegisterListBase):
    register_type: Literal[RegisterTypes.LLP_MEMBERS, "llp_members"] = (
        dataclasses.field(
            default=RegisterTypes.LLP_MEMBERS,
            metadata={"description": "The register type."},
        )
    )
    links: LinksListLLPMembers | None = dataclasses.field(
        default=None,
        metadata={"description": "A set of URLs related to the resource."},
    )


@dataclass
class Registers:
    directors: RegisterListDirectors | None = dataclasses.field(
        default=None, metadata={"description": "List of registered company directors."}
    )
    secretaries: RegisterListSecretaries | None = dataclasses.field(
        default=None,
        metadata={"description": "List of registered company secretaries."},
    )
    persons_with_significant_control: (
        RegisterListPersonsWithSignificantControl | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "List of registered company persons with significant control."
        },
    )
    usual_residential_address: RegisterListUsualResidentialAddress | None = (
        dataclasses.field(
            default=None, metadata={"description": "List of register addresses."}
        )
    )
    llp_usual_residential_address: RegisterListLLPUsualResidentialAddress | None = (
        dataclasses.field(
            default=None, metadata={"description": "List of register addresses."}
        )
    )
    members: RegisterListMembers | None = dataclasses.field(
        default=None, metadata={"description": "List of registered company members.."}
    )
    llp_members: RegisterListLLPMembers | None = dataclasses.field(
        default=None, metadata={"description": "List of registered llp members."}
    )


@dataclass
class CompanyRegister:
    links: LinksType | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A set of URLs related to the resource, including self."
        },
    )
    company_number: CompanyNumber | None = dataclasses.field(
        default=None,
        metadata={"description": "The company number of the register information."},
    )
    kind: Literal[ResponseKind.REGISTERS] = dataclasses.field(
        default=ResponseKind.REGISTERS,
        metadata={"description": "The kind of the response."},
    )
    registers: Registers | None = dataclasses.field(
        default=None,
        metadata={"description": "company registers information."},
    )
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the resource."},
    )
