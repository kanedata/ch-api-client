import dataclasses
import datetime as dt
from enum import StrEnum
from typing import Literal

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import (
    AddressBase,
    CompanyNumber,
    DateOfBirthBase,
    ItemLinkBase,
    LinkBase,
    ParametersBase,
)
from ch_api_client.models._shared import OfficerAddress, OfficerDateOfBirth
from ch_api_client.models.ch_enums import CompanyStatus, CompanySubtype, CompanyType
from ch_api_client.models.enums import Country, DescriptionIdentifier, ResponseKind


@dataclass
class SearchParameters(ParametersBase):
    q: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The search query string."},
    )
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
class AlphabeticalSearchParameters(SearchParameters):
    search_above: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The ordered_alpha_key_with_id used for alphabetical paging above."
        },
    )
    search_below: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The ordered_alpha_key_with_id used for alphabetical paging below."
        },
    )
    size: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The maximum number of results matching the search term(s) to return with a range of 1 to 100"
        },
    )


class DissolvedSearchType(StrEnum):
    ALPHABETICAL = "alphabetical"
    BEST_MATCH = "best-match"
    PREVIOUS_NAME_DISSOLVED = "previous-name-dissolved"


@dataclass
class DissolvedSearchParameters(AlphabeticalSearchParameters):
    search_type: DissolvedSearchType = dataclasses.field(
        default=DissolvedSearchType.ALPHABETICAL,
        metadata={
            "description": "Determines type of search. Options are alphabetical, best-match, previous-name-dissolved"
        },
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Used in best-match and previous-name-dissolved search-type"
        },
    )


@dataclass
class AdvancedSearchParameters(ParametersBase):
    company_name_includes: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The company name includes advanced search filter"},
    )
    company_name_excludes: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The company name excludes advanced search filter."},
    )
    company_status: list[str] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The company status advanced search filter. To search using multiple values, use a comma delimited list or multiple of the same key i.e. company_status=xxx&company_status=yyy"
        },
    )
    company_subtype: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The company subtype advanced search filter. To search using multiple values, use a comma delimited list or multiple of the same key i.e. company_subtype=xxx&company_subtype=yyy",
        },
    )
    company_type: list[str] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The company type advanced search filter. To search using multiple values, use a comma delimited list or multiple of the same key i.e. company_type=xxx&company_type=yyy",
        },
    )
    dissolved_from: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The dissolved from date advanced search filter"},
    )
    dissolved_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The dissolved to date advanced search filter"},
    )
    incorporated_from: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The incorporated from date advanced search filter"},
    )
    incorporated_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The incorporated to date advanced search filter"},
    )
    location: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The location advanced search filter"},
    )
    sic_codes: list[str] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The SIC codes advanced search filter. To search using multiple values, use a comma delimited list or multiple of the same key i.e. sic_codes=xxx&sic_codes=yyy",
        },
    )
    size: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The maximum number of results matching the search term(s) to return with a range of 1 to 5000"
        },
    )
    start_index: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The point at which results will start from i.e show search results from result 20 (used for paging)"
        },
    )


@dataclass
class LinksModel(ItemLinkBase):
    self: str = dataclasses.field(
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


@dataclass
class DissolvedRegisteredOfficeAddress(AddressBase):
    pass


@dataclass
class PreviousCompanyName:
    company_number: str = dataclasses.field(
        metadata={"description": "The company number of the dissolved company."}
    )
    name: str = dataclasses.field(
        metadata={"description": "The previous name of the company."}
    )
    ceased_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date that the company ceased being known under the company name."
        },
    )
    effective_from: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date that the company started being known under the company name."
        },
    )


@dataclass
class DissolvedCompany:
    company_name: str = dataclasses.field(
        metadata={
            "description": "The company name associated with the dissolved company."
        }
    )
    company_number: str = dataclasses.field(
        metadata={"description": "The company number of the dissolved company."}
    )
    company_status: str = dataclasses.field(
        metadata={"description": "The status of the company."}
    )
    ordered_alpha_key_with_id: str = dataclasses.field(
        metadata={
            "description": "The alphakey with it's id associated with the dissolved company."
        }
    )
    kind: Literal[ResponseKind.SEARCHRESULTS_DISSOLVEDCOMPANY] = dataclasses.field(
        default=ResponseKind.SEARCHRESULTS_DISSOLVEDCOMPANY,
        metadata={"description": "The type of search result."},
    )
    date_of_cessation: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date that the company was dissolved."},
    )
    date_of_creation: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date that the company was incorporated."},
    )
    registered_office_address: DissolvedRegisteredOfficeAddress | None = (
        dataclasses.field(default=None)
    )
    previous_company_names: list[PreviousCompanyName] | None = dataclasses.field(
        default=None
    )
    matched_previous_company_name: PreviousCompanyName | None = dataclasses.field(
        default=None
    )


@dataclass
class DissolvedTopHit(DissolvedCompany):
    pass


@dataclass
class DissolvedCompanySearch:
    etag: str | None = dataclasses.field(default=None)
    hits: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The number of hits returned on a best-match or previous-company-names search"
        },
    )
    kind: Literal[
        ResponseKind.SEARCH_DISSOLVED,
        ResponseKind.SEARCH_ALPHABETICALDISSOLVED,
        ResponseKind.SEARCH_PREVIOUSNAMEDISSOLVED,
    ] = dataclasses.field(
        default=ResponseKind.SEARCH_DISSOLVED,
        metadata={"description": "The type of search response returned."},
    )
    items: list[DissolvedCompany] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The results of the completed search."},
    )
    top_hit: DissolvedTopHit | None = dataclasses.field(
        default=None,
        metadata={"description": "The top hit of the search results."},
    )


@dataclass
class AlphabeticalCompanyLinks(LinkBase):
    company_profile: str = dataclasses.field(
        metadata={"description": "The link to the alphabetical company."}
    )


@dataclass
class AlphabeticalCompany:
    company_name: str = dataclasses.field(
        metadata={
            "description": "The company name associated with the dissolved company."
        }
    )
    company_number: str = dataclasses.field(
        metadata={"description": "The company number of the dissolved company."}
    )
    company_status: str = dataclasses.field(
        metadata={"description": "The status of the company."}
    )
    company_type: str = dataclasses.field(
        metadata={"description": "The type of company associated with the company"}
    )
    ordered_alpha_key_with_id: str = dataclasses.field(
        metadata={
            "description": "The alphakey with it's id associated with the dissolved company."
        }
    )
    kind: Literal[ResponseKind.SEARCHRESULTS_ALPHABETICALSEARCH] = dataclasses.field(
        default=ResponseKind.SEARCHRESULTS_ALPHABETICALSEARCH,
        metadata={"description": "The type of search result."},
    )
    links: AlphabeticalCompanyLinks | None = dataclasses.field(
        default=None,
        metadata={"description": "The links associated with the alphabetical company."},
    )


@dataclass
class AlphabeticalTopHit(AlphabeticalCompany):
    pass


@dataclass
class AlphabeticalCompanySearch:
    kind: Literal[
        ResponseKind.SEARCH_ALPHABETICALSEARCH,
        ResponseKind.SEARCH_ENHANCEDSEARCH,
    ] = dataclasses.field(
        default=ResponseKind.SEARCH_ALPHABETICALSEARCH,
        metadata={"description": "The type of search response returned."},
    )
    items: list[AlphabeticalCompany] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The results of the completed search."},
    )
    top_hit: AlphabeticalTopHit | None = dataclasses.field(
        default=None,
        metadata={"description": "The top hit of the search results."},
    )


@dataclass
class AdvancedCompanyLinks(AlphabeticalCompanyLinks):
    pass


@dataclass
class AdvancedRegisteredOfficeAddress(AddressBase):
    pass


@dataclass
class AdvancedCompany:
    company_name: str = dataclasses.field(
        metadata={
            "description": "The company name associated with the dissolved company."
        }
    )
    company_number: CompanyNumber = dataclasses.field(
        metadata={"description": "The company number of the dissolved company."}
    )
    company_status: CompanyStatus = dataclasses.field(
        metadata={"description": "The status of the company."}
    )
    company_type: CompanyType = dataclasses.field(
        metadata={"description": "The type of company associated with the company"}
    )
    company_subtype: CompanySubtype | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The subtype of the company associated with the company"
        },
    )
    kind: Literal[ResponseKind.SEARCH_RESULTS_COMPANY] = dataclasses.field(
        default=ResponseKind.SEARCH_RESULTS_COMPANY,
        metadata={"description": "The type of search result."},
    )
    links: AdvancedCompanyLinks | None = dataclasses.field(
        default=None,
        metadata={"description": "The link to the company"},
    )
    date_of_creation: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date of creation of the company."},
    )
    date_of_cessation: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date of cessation of the company."},
    )
    registered_office_address: AdvancedRegisteredOfficeAddress | None = (
        dataclasses.field(
            default=None,
            metadata={"description": "The registered office address of the company."},
        )
    )
    sic_codes: list[str] | None = dataclasses.field(
        default=None,
        metadata={"description": "SIC codes for this company"},
    )


@dataclass
class AdvancedTopHit(AdvancedCompany):
    pass


@dataclass
class AdvancedCompanySearch:
    hits: int = dataclasses.field(
        metadata={"description": "The number of matches found using advanced search"},
    )
    items: list[AdvancedCompany] = dataclasses.field(
        default_factory=list,
        metadata={"description": "The results of the completed search."},
    )
    top_hit: AdvancedTopHit | None = dataclasses.field(
        default=None,
        metadata={"description": "The top hit of the search results."},
    )
    kind: Literal[ResponseKind.SEARCH_ADVANCEDSEARCH] = dataclasses.field(
        default=ResponseKind.SEARCH_ADVANCEDSEARCH
    )
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the search response."},
    )
