import dataclasses
import datetime as dt
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import (
    AddressBase,
    CompanyNumber,
    DateOfBirthBase,
    ParametersBase,
)
from ch_api_client.models._shared import OfficerAddress, OfficerDateOfBirth
from ch_api_client.models.ch_enums import CompanyStatus, CompanyType
from ch_api_client.models.enums import Country, DescriptionIdentifier, ResponseKind


@dataclass
class SearchParameters(ParametersBase):
    items_per_page: int | None = dataclasses.field(
        default=None,
        metadata={"description": "The number of search results to return per page."},
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={"description": "The index of the first result item to return."},
    )


@dataclass
class CompanySearchParameters(SearchParameters):
    restrictions: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": 'Enumerable options to restrict search results. Space separate multiple restriction options to combine functionality. For a "company name availability" search use "active-companies legally-equivalent-company-name" together.'
        },
    )


@dataclass
class OfficerSearchParameters(SearchParameters):
    pass


@dataclass
class DisqualifiedOfficerSearchParameters(SearchParameters):
    pass


@dataclass
class LinksModel:
    self: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The URL of the resource being returned by the search item."
        },
    )


@dataclass
class MatchesModel:
    title: list[int] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "An array of character offset into the `title` string. These always occur in pairs and define the start and end of substrings in the member `title` that matched the search terms. The first character of the string is index 1."
        },
    )
    snippet: list[int] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "An array of character offset into the `snippet` string. These always occur in pairs and define the start and end of substrings in the member `snippet` that matched the search terms. The first character of the string is index 1."
        },
    )
    address_snippet: list[int] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "An array of character offset into the `address_snippet` string. These always occur in pairs and define the start and end of substrings in the member `address_snippet` that matched the search terms."
        },
    )


@dataclass
class RegisteredOfficeAddress(AddressBase):
    country: Country | None = dataclasses.field(
        default=None,
        metadata={"description": "The country."},
    )


@dataclass
class PersonsWithSignificantControlAddress(AddressBase):
    country: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The country."},
    )
    premises: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The property name or number."},
    )


@dataclass
class DisqualifiedOfficerAddress(AddressBase):
    country: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The country."},
    )
    premises: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The property name or number."},
    )


@dataclass
class PersonWithSignificantControlDateOfBirth(DateOfBirthBase):
    month: int = dataclasses.field(
        metadata={
            "description": "The month the person with significant control was born in."
        },
    )
    year: int = dataclasses.field(
        metadata={
            "description": "The year the person with significant control was born in."
        },
    )


@dataclass
class CommonSearch:
    items_per_page: int = dataclasses.field(
        metadata={"description": "The number of search items returned per page."}
    )
    start_index: int = dataclasses.field(
        metadata={
            "description": "The index into the entire result set that this result page starts."
        }
    )
    total_results: int = dataclasses.field(
        metadata={
            "description": "The number of further search results available for the current search."
        }
    )
    etag: str | None = dataclasses.field(
        default=None, metadata={"description": "The ETag of the resource"}
    )


@dataclass
class CommonSearchItems:
    title: str = dataclasses.field(
        metadata={"description": "The title of the search result."}
    )
    address_snippet: str = dataclasses.field(
        metadata={
            "description": "A single line address. This will be the address that matched within the indexed document or the primary address otherwise (as returned by the `address` member)."
        },
    )
    links: LinksModel = dataclasses.field(
        metadata={"description": "The URL of the search result."}
    )
    description: str | None = dataclasses.field(
        default=None, metadata={"description": "The result description."}
    )
    snippet: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Summary information for the result showing additional details that have matched."
        },
    )
    matches: MatchesModel | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A list of members and arrays of character offset defining substrings that matched the search terms."
        },
    )


@dataclass(kw_only=True)
class SearchItems(CommonSearchItems):
    kind: Literal[
        ResponseKind.SEARCHRESULTS_COMPANY,
        ResponseKind.SEARCHRESULTS_OFFICER,
        ResponseKind.SEARCHRESULTS_PERSONSWITHSIGNIFICANTCONTROL,
        ResponseKind.SEARCHRESULTS_DISQUALIFIEDOFFICER,
    ] = dataclasses.field(
        metadata={
            "description": "The type of search result. Refer to the full resource descriptions [CompanySearch resource](api/docs/company/company_number/CompanySearch-resource.html)  [OfficerSearch resource] (api/docs/company/company_number/OfficerSearch-resource.html) and [DisqualifiedOfficerSearch resource](api/docs/company/company_number/DisqualifiedOfficerSearch-resource.html) for the full list of members returned."
        },
    )
    address: RegisteredOfficeAddress = dataclasses.field(
        metadata={"description": "The address of the company's registered office."},
    )
    description_identifier: list[DescriptionIdentifier] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "An array of enumeration types that make up the search description. See search_descriptions_raw.yaml in api-enumerations"
        },
    )

    def __str__(self) -> str:
        return f"{self.kind}: {self.title}"


@dataclass(kw_only=True)
class CompanySearchItems(CommonSearchItems):
    kind: Literal[ResponseKind.SEARCHRESULTS_COMPANY] = dataclasses.field(
        metadata={
            "description": "The type of search result. Refer to the full resource descriptions [CompanySearch resource](api/docs/company/company_number/CompanySearch-resource.html)  [OfficerSearch resource] (api/docs/company/company_number/OfficerSearch-resource.html) and [DisqualifiedOfficerSearch resource](api/docs/company/company_number/DisqualifiedOfficerSearch-resource.html) for the full list of members returned."
        },
    )
    address: RegisteredOfficeAddress = dataclasses.field(
        metadata={"description": "The address of the company's registered office."},
    )
    description_identifier: (
        list[
            Literal[
                DescriptionIdentifier.INCORPORATED_ON,
                DescriptionIdentifier.REGISTERED_ON,
                DescriptionIdentifier.FORMED_ON,
                DescriptionIdentifier.DISSOLVED_ON,
                DescriptionIdentifier.CONVERTED_CLOSED_ON,
                DescriptionIdentifier.CLOSED_ON,
                DescriptionIdentifier.CLOSED,
                DescriptionIdentifier.FIRST_UK_ESTABLISHMENT_OPENED_ON,
                DescriptionIdentifier.OPENED_ON,
                DescriptionIdentifier.VOLUNTARY_ARRANGEMENT,
                DescriptionIdentifier.RECEIVERSHIP,
                DescriptionIdentifier.INSOLVENCY_PROCEEDINGS,
                DescriptionIdentifier.LIQUIDATION,
                DescriptionIdentifier.ADMINISTRATION,
                DescriptionIdentifier.REGISTERED,
                DescriptionIdentifier.REMOVED,
            ]
        ]
        | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "An array of enumeration types that make up the search description. See search_descriptions_raw.yaml in api-enumerations"
        },
    )
    company_number: CompanyNumber = dataclasses.field(
        metadata={
            "description": "The company registration / incorporation number of the company."
        },
    )
    date_of_creation: dt.date = dataclasses.field(
        metadata={"description": "The date the company was created."},
    )
    date_of_cessation: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the company ended."},
    )
    company_type: CompanyType = dataclasses.field(
        metadata={"description": "The company type."},
    )
    company_status: CompanyStatus = dataclasses.field(
        metadata={"description": "The company status."},
    )

    def __str__(self) -> str:
        return f"{self.kind}: {self.title}"


@dataclass(kw_only=True)
class OfficerSearchItems(CommonSearchItems):
    kind: Literal[ResponseKind.SEARCHRESULTS_OFFICER] = dataclasses.field(
        metadata={
            "description": "The type of search result. Refer to the full resource descriptions [CompanySearch resource](api/docs/company/company_number/CompanySearch-resource.html)  [OfficerSearch resource] (api/docs/company/company_number/OfficerSearch-resource.html) and [DisqualifiedOfficerSearch resource](api/docs/company/company_number/DisqualifiedOfficerSearch-resource.html) for the full list of members returned."
        },
    )
    date_of_birth: OfficerDateOfBirth | None = dataclasses.field(
        default=None,
        metadata={"description": "The officer date of birth details."},
    )
    appointment_count: int = dataclasses.field(
        metadata={"description": "The total number of appointments the officer has."},
    )
    description_identifiers: (
        list[
            Literal[
                DescriptionIdentifier.APPOINTMENT_COUNT, DescriptionIdentifier.BORN_ON
            ]
        ]
        | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "An array of enumeration types that make up the search description. See search_descriptions_raw.yaml in api-enumerations"
        },
    )

    address: OfficerAddress = dataclasses.field(
        metadata={"description": "The service address of the officer."},
    )

    def __str__(self) -> str:
        return f"{self.kind}: {self.title}"


@dataclass(kw_only=True)
class PersonsWithSignificantControlSearchItems(CommonSearchItems):
    kind: Literal[ResponseKind.SEARCHRESULTS_PERSONSWITHSIGNIFICANTCONTROL] = (
        dataclasses.field(
            metadata={
                "description": "The type of search result. Refer to the full resource descriptions [CompanySearch resource](api/docs/company/company_number/CompanySearch-resource.html)  [OfficerSearch resource] (api/docs/company/company_number/OfficerSearch-resource.html) and [DisqualifiedOfficerSearch resource](api/docs/company/company_number/DisqualifiedOfficerSearch-resource.html) for the full list of members returned."
            },
        )
    )
    date_of_birth: PersonWithSignificantControlDateOfBirth | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The person with significant control date of birth details."
        },
    )
    appointment_count: int = dataclasses.field(
        metadata={"description": "The total number of appointments the officer has."},
    )
    description_identifiers: (
        list[
            Literal[
                DescriptionIdentifier.NOTIFICATION_COUNT, DescriptionIdentifier.BORN_ON
            ]
        ]
        | None
    ) = dataclasses.field(
        default=None,
        metadata={
            "description": "An array of enumeration types that make up the search description. See search_descriptions_raw.yaml in api-enumerations"
        },
    )

    address: OfficerAddress = dataclasses.field(
        metadata={
            "description": "The service address of the person with significant control."
        },
    )

    def __str__(self) -> str:
        return f"{self.kind}: {self.title}"


@dataclass(kw_only=True)
class DisqualifiedOfficerSearchItems(CommonSearchItems):
    kind: Literal[ResponseKind.SEARCHRESULTS_DISQUALIFIEDOFFICER] = dataclasses.field(
        metadata={
            "description": "The type of search result. Refer to the full resource descriptions [CompanySearch resource](api/docs/company/company_number/CompanySearch-resource.html)  [OfficerSearch resource] (api/docs/company/company_number/OfficerSearch-resource.html) and [DisqualifiedOfficerSearch resource](api/docs/company/company_number/DisqualifiedOfficerSearch-resource.html) for the full list of members returned."
        },
    )
    date_of_birth: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The disqualified officer's date of birth."},
    )
    description_identifiers: list[Literal[DescriptionIdentifier.BORN_ON]] | None = (
        dataclasses.field(
            default=None,
            metadata={
                "description": "An array of enumeration types that make up the search description. See search_descriptions_raw.yaml in api-enumerations"
            },
        )
    )

    address: DisqualifiedOfficerAddress = dataclasses.field(
        metadata={
            "description": "The address of the disqualified officer as provided by the disqualifying authority."
        },
    )

    def __str__(self) -> str:
        return f"{self.kind}: {self.title}"


@dataclass
class Search(CommonSearch):
    kind: Literal[ResponseKind.SEARCH_ALL] = dataclasses.field(
        default=ResponseKind.SEARCH_ALL,
        metadata={"description": "The type of search response returned."},
    )
    items: list[SearchItems] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The list of search result items."},
    )


@dataclass
class CompanySearch(CommonSearch):
    kind: Literal[ResponseKind.SEARCH_COMPANIES] = dataclasses.field(
        default=ResponseKind.SEARCH_COMPANIES,
        metadata={"description": "The type of search response returned."},
    )
    items: list[CompanySearchItems] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The results of the completed search."},
    )


@dataclass
class OfficerSearch(CommonSearch):
    kind: Literal[ResponseKind.SEARCH_OFFICERS] = dataclasses.field(
        default=ResponseKind.SEARCH_OFFICERS,
        metadata={"description": "The type of search response returned."},
    )
    items: list[OfficerSearchItems] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The results of the completed search."},
    )


@dataclass
class PersonsWithSignificantControlSearch(CommonSearch):
    kind: Literal[ResponseKind.SEARCH_PERSONSWITHSIGNIFICANTCONTROL] = (
        dataclasses.field(
            default=ResponseKind.SEARCH_PERSONSWITHSIGNIFICANTCONTROL,
            metadata={"description": "The type of search response returned."},
        )
    )
    items: list[PersonsWithSignificantControlSearchItems] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The results of the completed search."},
    )


@dataclass
class DisqualifiedOfficerSearch(CommonSearch):
    kind: Literal[ResponseKind.SEARCH_DISQUALIFIEDOFFICER] = dataclasses.field(
        default=ResponseKind.SEARCH_DISQUALIFIEDOFFICER,
        metadata={"description": "The type of search response returned."},
    )
    items: list[DisqualifiedOfficerSearchItems] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The results of the completed search."},
    )
