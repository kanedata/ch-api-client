import dataclasses
from functools import wraps

import httpx2

from ch_api_client.models._base import CompanyNumber, ParametersBase
from ch_api_client.models.company_profile import (
    CompanyProfile,
    CompanyProfileParameters,
)
from ch_api_client.models.search import (
    CompanySearch,
    CompanySearchParameters,
    DisqualifiedOfficerSearch,
    DisqualifiedOfficerSearchParameters,
    OfficerSearch,
    OfficerSearchParameters,
    Search,
    SearchParameters,
)

CH_API_BASE_URL = "https://api.company-information.service.gov.uk"


def is_cli_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    setattr(wrapper, "_is_cli_method", True)

    return wrapper


class CompaniesHouseAPI:
    def __init__(self, api_key: str, session: httpx2.Client | None = None):
        self.api_key = api_key
        self.session = session or httpx2.Client()
        self.session.auth = (self.api_key, "")

    def _fetch_url(self, url: str, params: ParametersBase) -> dict:
        """Fetch a URL with the given parameters and return the JSON response."""
        response = self.session.get(url, params=dataclasses.asdict(params))
        response.raise_for_status()
        return response.json()

    @is_cli_method
    def get_company_profile(self, company_number: str) -> CompanyProfile:
        """
        Company profile

        Retrieve the company profile for the given company number.

        Args:
            company_number (str): The company number of the company profile to retrieve.

        Returns:
            CompanyProfile: The company profile information.
        """
        url = f"{CH_API_BASE_URL}/company/{company_number}"

        params = CompanyProfileParameters(company_number=CompanyNumber(company_number))
        return CompanyProfile(**self._fetch_url(url, params=params))

    @is_cli_method
    def get_search_all(
        self, q: str, items_per_page: int | None = None, start_index: int | None = None
    ) -> Search:
        """
        Search All

        Search companies, officers and disqualified officers

        Args:
            q (str): The term being searched for.
            items_per_page (int | None): The number of items to return per page.
            start_index (int | None): The index of the first item to return.

        Returns:
            Search: The search results.
        """
        url = f"{CH_API_BASE_URL}/search"
        params = SearchParameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
        )
        return Search(**self._fetch_url(url, params=params))

    @is_cli_method
    def get_search_companies(
        self,
        q: str,
        items_per_page: int | None = None,
        start_index: int | None = None,
        restrictions: str | None = None,
    ) -> CompanySearch:
        """
        Search companies

        Search company information

        Args:
            q (str): The term being searched for.
            items_per_page (int | None): The number of items to return per page.
            start_index (int | None): The index of the first item to return.
            restrictions (str | None): Enumerable options to restrict search results. Space separate multiple restriction options to combine functionality. For a "company name availability" search use "active-companies legally-equivalent-company-name" together.

        Returns:
            CompanySearch: The search results.
        """
        url = f"{CH_API_BASE_URL}/search/companies"
        params = CompanySearchParameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
            restrictions=restrictions,
        )
        return CompanySearch(**self._fetch_url(url, params=params))

    @is_cli_method
    def get_search_officers(
        self,
        q: str,
        items_per_page: int | None = None,
        start_index: int | None = None,
    ) -> OfficerSearch:
        """
        Search officers

        Search officer information

        Args:
            q (str): The term being searched for.
            items_per_page (int | None): The number of items to return per page.
            start_index (int | None): The index of the first item to return.

        Returns:
            OfficerSearch: The search results.
        """
        url = f"{CH_API_BASE_URL}/search/officers"
        params = OfficerSearchParameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
        )
        return OfficerSearch(**self._fetch_url(url, params=params))

    @is_cli_method
    def get_search_disqualified_officers(
        self,
        q: str,
        items_per_page: int | None = None,
        start_index: int | None = None,
    ) -> DisqualifiedOfficerSearch:
        """
        Search disqualified officers

        Search disqualified officer information

        Args:
            q (str): The term being searched for.
            items_per_page (int | None): The number of items to return per page.
            start_index (int | None): The index of the first item to return.

        Returns:
            DisqualifiedOfficerSearch: The search results.
        """
        url = f"{CH_API_BASE_URL}/search/disqualified-officers"
        params = DisqualifiedOfficerSearchParameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
        )
        return DisqualifiedOfficerSearch(**self._fetch_url(url, params=params))
