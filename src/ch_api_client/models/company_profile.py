import dataclasses
import datetime as dt

from pydantic.dataclasses import dataclass

from ch_api_client.models._base import (
    AccountingDateBase,
    AddressBase,
    CompanyNumber,
    ItemLinkBase,
    SICCode,
)
from ch_api_client.models.ch_enums import (
    AccountType,
    CompanyStatus,
    CompanyStatusDetail,
    CompanySubtype,
    CompanyType,
    CorporateAnnotationType,
    ForeignAccountType,
    Jurisdiction,
    PartialDataAvailable,
    TermsOfAccountPublication,
)
from ch_api_client.models.enums import Country


@dataclass
class LinksType(ItemLinkBase):
    persons_with_significant_control: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The URL of the persons with significant control list resource."
        },
    )
    persons_with_significant_control_statements: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The URL of the persons with significant control statements list resource."
        },
    )
    registers: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The URL of the registers resource for this company"},
    )
    uk_establishments: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The URL of the uk establishments list resource for this company."
        },
    )
    overseas: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The URL of the overseas details resource for this company."
        },
    )
    officers: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The URL of the company's officer list resource."},
    )
    insolvency: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The URL of the company's insolvency list resource."},
    )
    filing_history: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The URL of the company's filing history list resource."
        },
    )
    charges: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The URL of the company's charges list resource."},
    )
    exemptions: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The URL of the company's exemptions list resource."},
    )


@dataclass
class AccountingReferenceDate(AccountingDateBase):
    day: int = dataclasses.field(
        metadata={"description": "The Accounting Reference Date (ARD) day."},
    )
    month: int = dataclasses.field(
        metadata={"description": "The Accounting Reference Date (ARD) month."},
    )


@dataclass
class LastAccounts:
    made_up_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Deprecated. Please use accounts.last_accounts.period_end_on"
        },
    )
    period_end_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The last day of the most recently filed accounting period."
        },
    )
    period_start_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The first day of the most recently filed accounting period."
        },
    )
    type: AccountType | None = dataclasses.field(
        default=None,
        metadata={"description": "The type of the last company accounts filed."},
    )


@dataclass
class NextAccounts:
    due_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the next company accounts are due"},
    )
    overdue: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Flag indicating if the company accounts are overdue."
        },
    )
    period_end_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The last day of the next accounting period to be filed."
        },
    )
    period_start_on: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The first day of the next accounting period to be filed."
        },
    )


@dataclass
class AccountsInformation:
    overdue: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Deprecated. Please use accounts.next_accounts.overdue"
        },
    )
    next_made_up_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Deprecated. Please use accounts.next_accounts.period_end_on"
        },
    )
    accounting_reference_date: AccountingReferenceDate | None = dataclasses.field(
        default=None,
        metadata={"description": "The Accounting Reference Date (ARD) of the company."},
    )
    last_accounts: LastAccounts | None = dataclasses.field(
        default=None,
        metadata={"description": "The last company accounts filed."},
    )
    next_due: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Deprecated. Please use accounts.next_accounts.due_on"
        },
    )
    next_accounts: NextAccounts | None = dataclasses.field(
        default=None,
        metadata={"description": "The next company accounts filed."},
    )


@dataclass
class AnnualReturnInformation:
    last_made_up_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date the last annual return was made up to."},
    )
    next_due: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the next annual return is due. This member will only be returned if a confirmation statement has not been filed and the date is before 28th July 2016, otherwise refer to `confirmation_statement.next_due`"
        },
    )
    next_made_up_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date the next annual return should be made up to. This member will only be returned if a confirmation statement has not been filed and the date is before 30th July 2016, otherwise refer to `confirmation_statement.next_made_up_to`"
        },
    )
    overdue: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Flag indicating if the annual return is overdue."},
    )


@dataclass
class ConfirmationOfStatementInformation:
    last_made_up_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date to which the company last made a confirmation statement."
        },
    )
    next_due: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date by which the next confimation statement must be received."
        },
    )
    next_made_up_to: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date to which the company must next make a confirmation statement."
        },
    )
    overdue: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Flag indicating if the confirmation statement is overdue"
        },
    )


@dataclass
class OriginatingRegistry:
    name: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Identity of register in country of incorporation."},
    )
    country: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Country in which company was incorporated."},
    )


@dataclass
class AccountsRequired:
    foreign_account_type: ForeignAccountType | None = dataclasses.field(
        default=None,
        metadata={"description": "Type of accounting requirement that applies."},
    )
    terms_of_account_publication: TermsOfAccountPublication | None = dataclasses.field(
        default=None,
        metadata={"description": "Describes how the publication date is derived."},
    )


@dataclass
class AccountPeriodFrom(AccountingDateBase):
    day: int = dataclasses.field(
        metadata={
            "description": "Day on which accounting period starts under parent law."
        },
    )
    month: int = dataclasses.field(
        metadata={
            "description": "Month in which accounting period starts under parent law."
        },
    )


@dataclass
class AccountPeriodTo(AccountingDateBase):
    day: int = dataclasses.field(
        metadata={
            "description": "Day on which accounting period ends under parent law."
        },
    )
    month: int = dataclasses.field(
        metadata={
            "description": "Month in which accounting period ends under parent law."
        },
    )


@dataclass
class FileWithin:
    months: int = dataclasses.field(
        metadata={"description": "Number of months within which to file."},
    )


@dataclass
class AccountInformation:
    account_period_from: AccountPeriodFrom | None = dataclasses.field(
        default=None,
        metadata={"description": "Date account period starts under parent law."},
    )
    account_period_to: AccountPeriodTo | None = dataclasses.field(
        default=None,
        metadata={"description": "Date account period ends under parent law."},
    )
    must_file_within: FileWithin | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Time allowed from period end for disclosure of accounts under parent law."
        },
    )


@dataclass
class ForeignCompanyDetails:
    originating_registry: OriginatingRegistry | None = dataclasses.field(
        default=None,
        metadata={"description": "Company origin informations."},
    )
    registration_number: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Registration number in company of incorporation."},
    )
    governed_by: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Law governing the company in country of incorporation."
        },
    )
    company_type: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Legal form of the company in the country of incorporation."
        },
    )
    is_a_credit_finance_institution: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Is it a financial or credit institution."},
    )
    accounts: AccountInformation | None = dataclasses.field(
        default=None,
        metadata={"description": "Foreign company account information."},
    )
    business_activity: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Type of business undertaken by the company."},
    )
    accounting_requirement: AccountsRequired | None = dataclasses.field(
        default=None,
        metadata={"description": "Accounts requirement."},
    )


@dataclass
class RegisteredOfficeAddress(AddressBase):
    country: Country | None = dataclasses.field(
        default=None,
        metadata={"description": "The country."},
    )
    premises: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The property name or number."},
    )


@dataclass
class ServiceAddress(AddressBase):
    country: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The country e.g. United Kingdom."},
    )


@dataclass
class PreviousCompanyNames:
    name: str = dataclasses.field(
        metadata={"description": "The previous company name"},
    )
    effective_from: dt.date = dataclasses.field(
        metadata={"description": "The date from which the company name was effective."},
    )
    ceased_on: dt.date = dataclasses.field(
        metadata={"description": "The date on which the company name ceased."},
    )


@dataclass
class CorporateAnnotation:
    created_on: dt.date = dataclasses.field(
        metadata={
            "description": "The date on which the corporate annotation was created."
        },
    )
    type: CorporateAnnotationType = dataclasses.field(
        metadata={"description": "The type of corporate annotation."},
    )
    description: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The details of a corporate annotation which has a corporate_annotation.type of “other”."
        },
    )


@dataclass
class BranchCompanyDetails:
    business_activity: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Type of business undertaken by the UK establishment."
        },
    )
    parent_company_number: CompanyNumber | None = dataclasses.field(
        default=None,
        metadata={"description": "Parent company number."},
    )
    parent_company_name: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Parent company name."},
    )


@dataclass
class CompanyProfile:
    company_name: str = dataclasses.field(
        metadata={"description": "The name of the company."},
    )
    company_number: CompanyNumber = dataclasses.field(
        metadata={"description": "The number of the company."},
    )
    type: CompanyType = dataclasses.field(
        metadata={
            "description": "The type of the company.  \n For enumeration descriptions see `company_type` section in the [enumeration mappings](https://github.com/companieshouse/api-enumerations/blob/master/constants.yml)    "
        },
    )
    can_file: bool = dataclasses.field(
        metadata={"description": "Flag indicating whether this company can file."},
    )
    links: LinksType = dataclasses.field(
        metadata={
            "description": "A set of URLs related to the resource, including self."
        },
    )

    accounts: AccountsInformation | None = dataclasses.field(
        default=None,
        metadata={"description": "Company accounts information."},
    )
    annual_return: AnnualReturnInformation | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Annual return information. This member is only returned if a confirmation statement has not be filed."
        },
    )
    confirmation_statement: ConfirmationOfStatementInformation | None = (
        dataclasses.field(
            default=None,
            metadata={
                "description": "Confirmation statement information (N.B. refers to the Annual Statement where type is registered-overseas-entity)"
            },
        )
    )
    jurisdiction: Jurisdiction | None = dataclasses.field(
        default=None,
        metadata={"description": "The jurisdiction of the company."},
    )
    date_of_creation: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date when the company was created."},
    )
    date_of_cessation: dt.date | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date which the company was converted/closed, dissolved or removed. Please refer to company status to determine which."
        },
    )
    etag: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The ETag of the resource."},
    )
    has_been_liquidated: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Deprecated. Please use links.insolvency"},
    )
    has_charges: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Deprecated. Please use links.charges"},
    )
    is_community_interest_company: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Deprecated. Please use subtype"},
    )
    subtype: CompanySubtype | None = dataclasses.field(
        default=None,
        metadata={"description": "The subtype of the company. Possible values are:"},
    )
    partial_data_available: PartialDataAvailable | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Returned if Companies House is not the primary source of data for this company.\nFor enumeration descriptions see partial_data_available section in the enumeration mappings (https://github.com/companieshouse/api-enumerations/blob/master/constants.yml)."
        },
    )
    external_registration_number: str | None = dataclasses.field(
        default=None,
        metadata={"description": "The number given by an external registration body."},
    )
    foreign_company_details: ForeignCompanyDetails | None = dataclasses.field(
        default=None,
        metadata={"description": "Foreign company details."},
    )
    last_full_members_list_date: dt.date | None = dataclasses.field(
        default=None,
        metadata={"description": "The date of last full members list update."},
    )
    registered_office_address: RegisteredOfficeAddress | None = dataclasses.field(
        default=None,
        metadata={"description": "The address of the company's registered office."},
    )
    service_address: ServiceAddress | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The correspondence address of a Registered overseas entity"
        },
    )
    super_secure_managing_officer_count: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The total count of super secure managing officers for a `registered-overseas-entity`."
        },
    )
    sic_codes: list[SICCode] | None = dataclasses.field(
        default=None,
        metadata={"description": "SIC codes for this company."},
    )
    previous_company_names: list[PreviousCompanyNames] | None = dataclasses.field(
        default=None,
        metadata={"description": "The previous names of this company."},
    )
    corporate_annotation: CorporateAnnotation | None = dataclasses.field(
        default=None,
        metadata={
            "description": "A corporate level message published by Companies House about a company, or situations affecting the company, or its information."
        },
    )
    company_status: CompanyStatus | None = dataclasses.field(
        default=None,
        metadata={"description": "The status of the company."},
    )
    company_status_detail: CompanyStatusDetail | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Extra details about the status of the company.  \n For enumeration descriptions see `company_status_detail` section in the [enumeration mappings](https://github.com/companieshouse/api-enumerations/blob/master/constants.yml).  "
        },
    )
    has_insolvency_history: bool | None = dataclasses.field(
        default=None,
        metadata={"description": "Deprecated. Please use links.insolvency"},
    )
    undeliverable_registered_office_address: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Flag indicating whether post can be delivered to the registered office."
        },
    )
    registered_office_is_in_dispute: bool | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Flag indicating registered office address as been replaced."
        },
    )
    branch_company_details: BranchCompanyDetails | None = dataclasses.field(
        default=None,
        metadata={"description": "UK branch of a foreign company."},
    )
