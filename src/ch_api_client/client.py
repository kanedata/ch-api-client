import dataclasses
import datetime as dt
from functools import wraps

import httpx2

from ch_api_client.models._base import CompanyNumber, ParametersBase
from ch_api_client.models.company_officer_list import (
    CompanyOfficerListParameters,
    OfficerList,
    OfficerSummary,
    OrderBy,
    RegisterType,
    RegisterView,
)
from ch_api_client.models.company_profile import CompanyProfile
from ch_api_client.models.document import ContentType, DocumentMetadata
from ch_api_client.models.filing_history import (
    AnnualAccount,
    AnnualAccountList,
    FilingHistoryItem,
    FilingHistoryList,
    FilingHistoryListParameters,
)
from ch_api_client.models.registered_office_address import RegisteredOfficeAddress
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

COMPANY_API_BASE_URL = "https://api.company-information.service.gov.uk"
DOCUMENT_API_BASE_URL = "https://document-api.company-information.service.gov.uk"


def is_cli_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    setattr(wrapper, "_is_cli_method", True)  # noqa: B010

    return wrapper


class CompaniesHouseAPI:
    def __init__(
        self,
        api_key: str,
        session: httpx2.Client | None = None,
        base_url: str = COMPANY_API_BASE_URL,
    ):
        self.api_key = api_key
        self.session = session or httpx2.Client()
        self.session.auth = (self.api_key, "")
        self.base_url = base_url

    def _fetch_url(
        self,
        url: str,
        params: ParametersBase | None = None,
        base_url: str | None = None,
    ) -> dict:
        """Fetch a URL with the given parameters and return the JSON response."""
        if base_url is None:
            base_url = self.base_url

        if params is None:
            params_dict = {}
        else:
            params_dict = {
                k: v for k, v in dataclasses.asdict(params).items() if v is not None
            }
        response = self.session.get(f"{base_url}{url}", params=params_dict)
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
        url = f"/company/{company_number}"
        return CompanyProfile(**self._fetch_url(url))

    @is_cli_method
    def get_registered_office_address(
        self, company_number: str
    ) -> RegisteredOfficeAddress:
        """
        Get the current registered office address of a company

        Args:
            company_number (str): Company number for registered office address

        Returns:
            RegisteredOfficeAddress: The registered officer address information.
        """
        # Example implementation:
        url = f"/company/{company_number}/registered-office-address"
        return RegisteredOfficeAddress(**self._fetch_url(url))

    @is_cli_method
    def get_company_officers(
        self,
        company_number: str,
        items_per_page: int | None = None,
        register_type: RegisterType | None = None,
        register_view: RegisterView | None = None,
        start_index: int | None = None,
        order_by: OrderBy | None = None,
    ) -> OfficerList:
        """
        Company Officers

        List of all company officers

        Args:
            company_number (str): The company number of the officer list being requested.
            items_per_page (int | None): The number of officers to return per page.
            register_type (RegisterType | None): The register_type determines which officer type is returned for the registers view.The register_type field will only work if registers_view is set to true
            register_view (RegisterView | None): Display register specific information. If given register is held at Companies House, registers_view set to true and correct register_type specified, only active officers will be returned. Defaults to false
            start_index (int | None): The offset into the entire result set that this page starts.
            order_by (OrderBy | None): The field by which to order the result set.

        Returns:
            OfficerList: The list of company officers.
        """
        url = f"/company/{company_number}/officers"

        params = CompanyOfficerListParameters(
            items_per_page=items_per_page,
            register_type=register_type,
            register_view=register_view,
            start_index=start_index,
            order_by=order_by,
        )
        return OfficerList(**self._fetch_url(url, params=params))

    @is_cli_method
    def get_company_officer_appointment(
        self,
        company_number: str,
        appointment_id: str,
    ) -> OfficerSummary:
        """
        Get a company officer appointment

        Get details of an individual company officer appointment

        Args:
            company_number (str): The company number of the officer list being requested.
            appointment_id (str): The appointment id of the company officer appointment being requested.

        Returns:
            OfficerSummary: The details of the company officer appointment.
        """
        url = f"/company/{company_number}/appointments/{appointment_id}"
        return OfficerSummary(**self._fetch_url(url))

    def get_company_registers(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    @is_cli_method
    def get_filing_history_list(
        self,
        company_number: str,
        category: str | None = None,
        items_per_page: int | None = None,
        start_index: int | None = None,
    ):
        """
        filingHistoryList resource

        Get the filing history list of a company

        Args:
            company_number (str): The company number that the single filing is required for.
            category (str): One or more comma-separated categories to filter by (inclusive).
            items_per_page (int): The number of filing history items to return per page.
            start_index (int): The index into the entire result set that this result page starts.

        Returns:
            FilingHistoryList: Filing history items resource returned
        """
        url = f"/company/{company_number}/filing-history"
        params = FilingHistoryListParameters(
            category=category,
            items_per_page=items_per_page,
            start_index=start_index,
        )
        return FilingHistoryList(**self._fetch_url(url, params=params))

    @is_cli_method
    def get_annual_account_list(self, company_number: str) -> AnnualAccountList:
        """
        Get a list of Annual Accounts of a company

        Args:
            company_number (str): The company number that the annual account list is required for.

        Returns:
            AnnualAccountList: The list of annual accounts for the company.
        """
        filing_history = self.get_filing_history_list(
            company_number=company_number, category="accounts"
        )
        if not filing_history.items:
            raise ValueError("No filing history items found for the company.")
        annual_accounts = AnnualAccountList()
        annual_accounts.items = []
        for item in filing_history.items:
            if (
                item.description_values
                and item.document_id
                and item.description_values.made_up_date
            ):
                doc_metadata = self.get_document_metadata(document_id=item.document_id)
                annual_accounts.items.append(
                    AnnualAccount(
                        company_number=CompanyNumber(company_number),
                        financial_year_end=item.description_values.made_up_date,
                        document_id=doc_metadata.document_id if doc_metadata else None,
                        type=item.description,
                        has_ixbrl=doc_metadata.has_ixbrl if doc_metadata else None,
                        has_pdf=doc_metadata.has_pdf if doc_metadata else None,
                    )
                )
        return annual_accounts

    @is_cli_method
    def get_annual_account(
        self, company_number: str, financial_year_end: dt.date
    ) -> AnnualAccount:
        """
        Get the annual account of a company

        Args:
            company_number (str): The company number that the annual account is required for.
            financial_year_end (dt.date | dt.datetime): The financial year end date of the annual account being requested.

        Returns:
            AnnualAccount: The details of the annual account.
        """
        if isinstance(financial_year_end, dt.datetime):
            financial_year_end = financial_year_end.date()
        if isinstance(financial_year_end, str):
            financial_year_end = dt.datetime.strptime(
                financial_year_end, "%Y-%m-%d"
            ).date()
        filing_history = self.get_filing_history_list(
            company_number=company_number, category="accounts"
        )
        if not filing_history.items:
            raise ValueError("No filing history items found for the company.")
        for item in filing_history.items:
            if (
                item.description_values
                and item.document_id
                and item.description_values.made_up_date == financial_year_end
            ):
                doc_metadata = self.get_document_metadata(document_id=item.document_id)
                return AnnualAccount(
                    company_number=CompanyNumber(company_number),
                    financial_year_end=financial_year_end,
                    document_id=doc_metadata.document_id if doc_metadata else None,
                    type=item.description,
                    has_ixbrl=doc_metadata.has_ixbrl if doc_metadata else None,
                    has_pdf=doc_metadata.has_pdf if doc_metadata else None,
                )
        raise ValueError(
            "No filing history item found for the specified financial year end."
        )

    @is_cli_method
    def get_annual_account_document(
        self,
        company_number: str,
        financial_year_end: dt.date,
        content_type: ContentType = ContentType.PDF,
    ) -> bytes:
        """
        Get the annual account document for a company financial year end

        Args:
            company_number (str): The company number that the annual account is required for.
            financial_year_end (dt.date | dt.datetime): The financial year end date of the annual account being requested.

        Returns:
            bytes: The content of the annual account document.
        """
        info = self.get_annual_account(
            company_number=company_number, financial_year_end=financial_year_end
        )
        if not info.document_id:
            raise ValueError("No document ID found for the specified annual account.")
        if content_type in (ContentType.XHTML, ContentType.XML) and not info.has_ixbrl:
            raise ValueError(
                "The requested content type is not available for this annual account."
            )
        if content_type == ContentType.PDF and not info.has_pdf:
            raise ValueError("No PDF version available for this annual account.")
        return self.get_document(
            document_id=info.document_id, content_type=content_type
        )

    @is_cli_method
    def get_filing_history(
        self, company_number: str, transaction_id: str
    ) -> FilingHistoryItem:
        """
        filingHistoryItem resource

        Get the filing history item of a company

        Args:
            company_number (str): The company number that the single filing is required for.
            transaction_id (str): The transaction id that the filing history is required for.

        Returns:
            FilingHistoryItem: Filing history items resource returned
        """
        url = f"/company/{company_number}/filing-history/{transaction_id}"
        return FilingHistoryItem(**self._fetch_url(url))

    @is_cli_method
    def get_document_metadata(self, document_id: str) -> DocumentMetadata:
        """
        Fetch a document's metadata

        Args:
            document_id (str): The document id that the metadata is required for.

        Returns:
            DocumentMetadata: The metadata of the filing history document.
        """
        url = f"/document/{document_id}"
        return DocumentMetadata(**self._fetch_url(url, base_url=DOCUMENT_API_BASE_URL))

    def get_document(
        self,
        document_id: str,
        document_metadata: DocumentMetadata | None = None,
        content_type: ContentType | None = None,
    ) -> bytes:
        """
        Fetch the content of a document given its metadata.

        Args:
            document_id (str): The ID of the document to fetch.
            document_metadata (DocumentMetadata | None): The metadata of the document to fetch.
            content_type (ContentType | None): The desired content type of the document.

        Returns:
            bytes: The content of the document.
        """
        url = f"{DOCUMENT_API_BASE_URL}/document/{document_id}/content"
        headers = {}
        if content_type:
            if (
                document_metadata
                and document_metadata.resources
                and (content_type.value not in document_metadata.resources)
            ):
                raise ValueError(
                    f"Content type {content_type.value} not available in document resources."
                )
            headers["Accept"] = content_type.value
        elif document_metadata:
            if document_metadata.resources and len(document_metadata.resources) == 1:
                headers["Accept"] = next(iter(document_metadata.resources.keys()))
            elif document_metadata.resources and len(document_metadata.resources) > 1:
                raise ValueError(
                    "Multiple content types available in document resources. Please specify a content type."
                )
        response = self.session.get(url, headers=headers, follow_redirects=True)
        response.raise_for_status()
        return response.content

    def get_exemptions(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_charge_list(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_charge_details(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_insolvency_case(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_uk_establishments(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_list(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_individual(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_individual_bo(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_corporate_entity(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_corporate_entity_bo(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_legal_person(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_legal_person_bo(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_super_secure(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_super_secure_bo(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_statements_list(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_statements_details(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_corporate_officer(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_natural_officer(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_officer_appointment_list(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_company_psc_notification_list(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

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
        url = "/search"
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
        url = "/search/companies"
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
        url = "/search/officers"
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
        url = "/search/disqualified-officers"
        params = DisqualifiedOfficerSearchParameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
        )
        return DisqualifiedOfficerSearch(**self._fetch_url(url, params=params))

    def get_search_dissolved(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_search_alphabetical(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")

    def get_search_advanced(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
