import datetime as dt
import json
import re
from importlib import resources

import click
import httpx2
from dotenv import load_dotenv
from faker import Faker
from faker.providers import BaseProvider

import ch_api_client.tests.fixtures
from ch_api_client import CompaniesHouseAPI
from ch_api_client.models.search import DissolvedSearchType

load_dotenv()

NON_PERSONAL_INFO_KEYS = (
    "accounting_reference_date",
    "accounts",
    "active_count",
    "application/pdf",
    "appointment_count",
    "appointments",
    "barcode",
    "can_file",
    "category",
    "ceased_count",
    "charge_number",
    "charges",
    "classification",
    "company_number",
    "company_profile",
    "company_status",
    "company_type",
    "content_length",
    "country_of_residence",
    "created_at",
    "description_identifier",
    "description_identifiers",
    "description_values",
    "description",
    "disclosure_transparency_rules_chapter_five_applies",
    "document_metadata",
    "document",
    "etag",
    "exempt_from",
    "exempt_to",
    "exemption_type",
    "exemptions",
    "filename",
    "filing_history_status",
    "filing_history",
    "filing_type",
    "filing",
    "former_names",
    "has_charges",
    "has_insolvency_history",
    "hits",
    "inactive_count",
    "is_pre_1992_appointment",
    "items_per_page",
    "items",
    "jurisdiction",
    "kind",
    "last_accounts",
    "links",
    "matches",
    "nationality",
    "officer_role",
    "officer",
    "officers",
    "page_number",
    "pages",
    "paper_filed",
    "part_satisfied_count",
    "particulars",
    "persons_entitled",
    "previous_company_names",
    "psc_exempt_as_trading_on_uk_regulated_market",
    "registered_office_is_in_dispute",
    "res_type",
    "resigned_count",
    "resolutions",
    "resources",
    "satisfied_count",
    "satisfied_on",
    "secured_details",
    "self",
    "sic_codes",
    "significant_date_type",
    "snippet",
    "start_index",
    "status",
    "subcategory",
    "top_hit",
    "total_count",
    "total_results",
    "transaction_id",
    "transactions",
    "type",
    "unfiltered_count",
    "cases",
    "dates",
    "number",
    "role",
    "practitioners",
    "name_elements",
    "natures_of_control",
    "ceased",
    "identity_verification_details",
    "persons_with_significant_control",
    "notifications",
)

DATE_KEYS = (
    "date_of_creation",
    "date_of_cessation",
    "resigned_on",
    "appointed_on",
    "made_up_to",
    "period_end_on",
    "last_full_members_list_date",
    "appointed_before",
    "date",
    "termination_date",
    "action_date",
    "appointment_date",
    "change_date",
    "made_up_date",
    "significant_date",
    "effective_from",
    "ceased_on",
    "created_on",
    "delivered_on",
    "ceased_to_act_on",
    "notified_on",
    "appointment_verification_end_on",
    "appointment_verification_start_on",
)

URL_RE_MATCH = re.compile(r"^/[A-Za-z0-9_\-\/]+$")


def get_fixture_filename(url: httpx2.URL) -> str:
    filename = url.path.replace("/", "_").strip("_")
    if re.match(r"^company_[0-9A-Z]{8}_registered-office-address$", filename):
        return "get_registered_office_address.json"
    if re.match(r"^company_[0-9A-Z]{8}_appointments_.*$", filename):
        return "get_company_officer_appointment.json"
    if re.match(r"^company_[0-9A-Z]{8}_officers$", filename):
        return "get_company_officers.json"
    if re.match(r"^company_[0-9A-Z]{8}_filing-history_.*$", filename):
        return "get_filing_history.json"
    if re.match(r"^company_[0-9A-Z]{8}_filing-history$", filename):
        return "get_filing_history_list.json"
    if re.match(r"^company_[0-9A-Z]{8}_exemptions$", filename):
        return "get_exemptions.json"
    if re.match(r"^company_[0-9A-Z]{8}_charges$", filename):
        return "get_charge_list.json"
    if re.match(r"^company_[0-9A-Z]{8}_insolvency$", filename):
        return "get_insolvency_case.json"
    if re.match(r"^company_[0-9A-Z]{8}_uk-establishments$", filename):
        return "get_company_uk_establishments.json"
    if re.match(r"^company_[0-9A-Z]{8}_persons-with-significant-control$", filename):
        return "get_company_psc_list.json"
    if re.match(r"^company_[0-9A-Z]{8}$", filename):
        return "get_company_profile.json"
    if re.match(r"^document_.*$", filename):
        return "get_document_metadata.json"
    return f"{filename}.json"


class CHProvider(BaseProvider):
    def company_number(self):
        return self.random_element(
            [
                self.numerify("########"),
                self.numerify("########"),
                self.numerify("########"),
                self.numerify("########"),
                self.numerify("########"),
                self.bothify("??######").upper(),
            ]
        )


def replace_address_details(data, faker: Faker):
    if not isinstance(data, dict):
        return data
    new_data = {}
    for k, v in data.items():
        if k == "address_line_1":
            new_data[k] = faker.secondary_address()
        elif k == "address_line_2":
            new_data[k] = faker.street_name()
        elif k == "locality":
            new_data[k] = faker.city()
        elif k == "po_box":
            new_data[k] = faker.building_number()
        elif k == "postal_code":
            new_data[k] = faker.postcode()
        elif k == "care_of":
            new_data[k] = faker.name()
        elif k == "region":
            new_data[k] = faker.administrative_unit()
        elif k == "country":
            new_data[k] = faker.current_country()
        elif k == "premises":
            new_data[k] = faker.building_number()
        elif isinstance(v, str):
            new_data[k] = "REDACTED"
        else:
            new_data[k] = replace_address_details(v, faker)
    return new_data


def replace_company_number(
    data, company_number: str | None = None, fake_company_number: str | None = None
):
    if (
        isinstance(data, str)
        and company_number is not None
        and fake_company_number is not None
        and company_number in data
    ):
        return data.replace(company_number, fake_company_number)
    return data


def recursive_replace_personal_info(
    data,
    faker: Faker,
    company_number: str | None = None,
    fake_company_number: str | None = None,
    url: httpx2.URL | None = None,
):
    if isinstance(data, dict):
        if company_number is None and "company_number" in data:
            company_number = data["company_number"]
            fake_company_number = (
                faker.company_number()
            )  # Use the CHProvider to generate a fake company number
        new_data = {}
        for k, v in data.items():
            v = replace_company_number(v, company_number, fake_company_number)
            if isinstance(v, str) and URL_RE_MATCH.match(v):
                v = "/URL/REDACTED"
            if k in (
                "address",
                "registered_office_address",
                "undeliverable_registered_office_address",
            ):
                new_data[k] = replace_address_details(v, faker)
                if "address_snippet" in data:
                    new_data["address_snippet"] = ", ".join(
                        v
                        for k, v in new_data["address"].items()
                        if isinstance(v, str) and v.strip()
                    )
            elif k in ("old_address", "new_address"):
                new_data[k] = ", ".join(faker.address().splitlines())
            elif k in ("title", "company_name"):
                new_data[k] = faker.company()
            elif k in ("name", "officer_name"):
                new_data[k] = faker.name()
            elif k in ("surname",):
                new_data[k] = faker.last_name()
            elif k in ("forename", "middle_name"):
                new_data[k] = faker.first_name()
            elif k == "address_line_1":
                new_data[k] = faker.secondary_address()
            elif k == "address_line_2":
                new_data[k] = faker.street_name()
            elif k == "locality":
                new_data[k] = faker.city()
            elif k == "po_box":
                new_data[k] = faker.building_number()
            elif k == "postal_code":
                new_data[k] = faker.postcode()
            elif k == "care_of":
                new_data[k] = faker.name()
            elif k == "region":
                new_data[k] = faker.administrative_unit()
            elif k == "country":
                new_data[k] = faker.current_country()
            elif k == "premises":
                new_data[k] = faker.building_number()
            elif k == "ordered_alpha_key_with_id":
                new_data[k] = faker.bothify(text="?????????:###########")
            elif k == "person_number":
                new_data[k] = faker.numerify(text="############")
            elif k in DATE_KEYS and v:
                try:
                    current_date = dt.datetime.strptime(data[k], "%Y-%m-%d")
                    try:
                        new_date = current_date + dt.timedelta(
                            days=faker.random_int(min=1, max=30)
                        )
                    except OverflowError:
                        new_date = current_date
                except ValueError:
                    new_data[k] = v
                else:
                    new_data[k] = new_date.strftime("%Y-%m-%d")
            elif k == "etag":
                new_data[k] = faker.hexify(
                    text="^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                )
            elif k == "day":
                new_data[k] = faker.random_int(min=1, max=31)
            elif k == "month":
                new_data[k] = faker.random_int(min=1, max=12)
            elif k == "date_of_birth":
                new_data[k] = {
                    "month": faker.random_int(min=1, max=12),
                    "year": faker.random_int(min=1900, max=2000),
                }
            elif k == "address_snippet":
                continue
            elif k in NON_PERSONAL_INFO_KEYS:
                new_data[k] = recursive_replace_personal_info(
                    v, faker, company_number, fake_company_number, url=url
                )
            else:
                print(f"Processing key: {k}")
                new_data[k] = recursive_replace_personal_info(
                    v, faker, company_number, fake_company_number, url=url
                )
        return new_data
    elif isinstance(data, list):
        new_data = [
            recursive_replace_personal_info(
                item, faker, company_number, fake_company_number, url=url
            )
            for item in data
        ]
        return new_data
    data = replace_company_number(data, company_number, fake_company_number)
    return data


def create_fixture(response: httpx2.Response):
    faker = Faker("en_GB")
    faker.add_provider(CHProvider)
    url = response.request.url
    filename = get_fixture_filename(url)
    output_file = resources.files(ch_api_client.tests.fixtures).joinpath(filename)
    print(f"Fetching URL: {response.request.url}")
    print(f"Saving fixture to: {output_file}")
    with (
        resources.as_file(output_file) as save_fixture,
        open(save_fixture, "w") as f,
    ):
        response.read()
        if response.content:
            data = recursive_replace_personal_info(response.json(), faker, url=url)
            json.dump(data, f)


@click.command()
@click.option(
    "--api-key",
    help="Your Companies House API key.",
    envvar="CH_API_KEY",
)
@click.option(
    "--test-company-number",
    help="The test company number.",
    envvar="TEST_COMPANY_NUMBER",
)
@click.option(
    "--test-insolvent-company-number",
    help="The test insolvent company number.",
    envvar="TEST_INSOLVENT_COMPANY_NUMBER",
)
@click.option(
    "--test-search-query",
    help="The test search query.",
    envvar="TEST_SEARCH_QUERY",
)
def main(
    api_key: str,
    test_company_number: str,
    test_insolvent_company_number: str,
    test_search_query: str,
):
    session = httpx2.Client(event_hooks={"response": [create_fixture]})
    api_client = CompaniesHouseAPI(api_key=api_key, session=session)

    # company profile endpoints
    api_client.get_company_profile(test_company_number)
    # api_client.get_company_registers(test_company_number)
    api_client.get_registered_office_address(test_company_number)
    officer_list = api_client.get_company_officers(test_company_number)
    appointment_id = officer_list.items[0].links.self.split("/")[-1]  # type: ignore
    api_client.get_company_officer_appointment(
        company_number=test_company_number,
        appointment_id=appointment_id,
    )
    api_client.get_exemptions(test_company_number)
    api_client.get_charge_list(test_company_number)
    api_client.get_insolvency_case(test_insolvent_company_number)
    api_client.get_company_uk_establishments(test_company_number)
    api_client.get_company_psc_list(test_company_number)

    # filing history
    filing_history = api_client.get_filing_history_list(test_company_number)
    transaction_id = filing_history.items[0].transaction_id  # type: ignore
    assert isinstance(transaction_id, str)
    filing_history_item = api_client.get_filing_history(
        test_company_number, transaction_id
    )
    assert isinstance(filing_history_item.document_id, str)
    api_client.get_document_metadata(filing_history_item.document_id)

    # search endpoints
    api_client.get_search_all(test_search_query)
    api_client.get_search_companies(test_search_query)
    api_client.get_search_officers(test_search_query)
    api_client.get_search_disqualified_officers(test_search_query)
    api_client.get_search_dissolved(
        test_search_query, search_type=DissolvedSearchType.BEST_MATCH
    )
    api_client.get_search_alphabetical(test_search_query)
    api_client.get_search_advanced(test_search_query, company_type=["ltd", "plc"])


if __name__ == "__main__":
    main()
