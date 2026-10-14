# Companies House API Client

A client for accessing the [Companies House API](https://developer-specs.company-information.service.gov.uk/).

The library contains a Client class which is initialised with your API key. The client object methods return 
dataclasses that match the specification. 

## Usage

Import the library and initialise with an API key.

```python
import os
from ch_api_client import CompaniesHouseAPI

CH_API_KEY = os.environ.get("CH_API_KEY")
COMPANY_NUMBER = "12345678"

api = CompaniesHouseAPI(CH_API_KEY)

company = api.get_company_profile(COMPANY_NUMBER)
print(company.company_number)
# prints "12345678"
```

## Command line

The library can also be used via the command line. It prints a JSON representation of 
the returned object (if the result has multiple items like a search query it prints each
result on a separate line).

```sh
ch-api-client get-search-all test
```

Returns (first item)

```json
{"title":"TEST","address_snippet":"Test, Test, Test, United Kingdom, TEST","links":{"self":"/officers/LtWn5hrTi5yaKeOCdPr7xFBITxI/appointments"},"description":"Total number of appointments 1","snippet":"","matches":{"title":null,"snippet":[],"address_snippet":null},"kind":"searchresults#officer","address":{"address_line_1":"Test","address_line_2":null,"locality":"Test","po_box":null,"postal_code":"TEST","care_of":null,"region":null,"country":"United Kingdom"},"description_identifier":null}
```

## Methods implemented

From the [Companies House Public Data API](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference)

| Method                                | Url                                                                                                              | Returned Object             | Implemented |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------|-----------------------------|-------------|
| `get_company_profile`                 | `/company/{company_number}`                                                                                      | `CompanyProfile`            | Y           |
| `get_company_address`                 | `/company/{company_number}/registered-office-address`                                                            |                             |             |
| `get_company_officers`                | `/company/{company_number}/officers`                                                                             | `OfficerList`               | Y           |
| `get_company_officer_appointment`     | `/company/{company_number}/appointments/{appointment_id}`                                                        | `OfficerSummary`            | Y           |
| `get_company_registers`               | `/company/{company_number}/registers`                                                                            |                             |             |
| `get_filing_history`                  | `/company/{company_number}/filing-history/{transaction_id}`                                                      | `FilingHistoryItem`         | Y           |
| `get_filing_history_list`             | `/company/{company_number}/filing-history`                                                                       | `FilingHistoryList`         | Y           |
| `get_exemptions`                      | `/company/{company_number}/exemptions`                                                                           |                             |             |
| `get_charge_list`                     | `/company/{company_number}/charges`                                                                              |                             |             |
| `get_charge_details`                  | `/company/{company_number}/charges/{charge_id}`                                                                  |                             |             |
| `get_insolvency_case`                 | `/company/{company_number}/insolvency`                                                                           |                             |             |
| `get_company_uk_establishments`       | `/company/{company_number}/uk-establishments`                                                                    |                             |             |
| `get_company_psc_list`                | `/company/{company_number}/persons-with-significant-control`                                                     |                             |             |
| `get_company_psc_individual`          | `/company/{company_number}/persons-with-significant-control/individual/{notification_id}`                        |                             |             |
| `get_company_psc_individual_bo`       | `/company/{company_number}/persons-with-significant-control/individual-beneficial-owner/{notification_id}`       |                             |             |
| `get_company_psc_corporate_entity`    | `/company/{company_number}/persons-with-significant-control/corporate-entity/{notification_id}`                  |                             |             |
| `get_company_psc_corporate_entity_bo` | `/company/{company_number}/persons-with-significant-control/corporate-entity-beneficial-owner/{notification_id}` |                             |             |
| `get_company_psc_legal_person`        | `/company/{company_number}/persons-with-significant-control/legal-person/{notification_id}`                      |                             |             |
| `get_company_psc_legal_person_bo`     | `/company/{company_number}/persons-with-significant-control/legal-person-beneficial-owner/{notification_id}`     |                             |             |
| `get_company_psc_super_secure`        | `/company/{company_number}/persons-with-significant-control/super-secure/{super_secure_id}`                      |                             |             |
| `get_company_psc_super_secure_bo`     | `/company/{company_number}/persons-with-significant-control/super-secure-beneficial-owner/{super_secure_id}`     |                             |             |
| `get_company_psc_statements_list`     | `/company/{company_number}/persons-with-significant-control-statements`                                          |                             |             |
| `get_company_psc_statements_details`  | `/company/{company_number}/persons-with-significant-control-statements/{statement_id}`                           |                             |             |
| `get_corporate_officer`               | `/disqualified-officers/corporate/{officer_id}`                                                                  |                             |             |
| `get_natural_officer`                 | `/disqualified-officers/natural/{officer_id}`                                                                    |                             |             |
| `get_officer_appointment_list`        | `/officers/{officer_id}/appointments`                                                                            |                             |             |
| `get_company_psc_notification_list`   | `/persons-with-significant-control/{psc_id}/notifications`                                                       |                             |             |
| `get_search_all`                      | `/search`                                                                                                        | `Search`                    | Y           |
| `get_search_companies`                | `/search/companies`                                                                                              | `CompanySearch`             | Y           |
| `get_search_officers`                 | `/search/officers`                                                                                               | `OfficerSearch`             | Y           |
| `get_search_disqualified_officers`    | `/search/disqualified-officers`                                                                                  | `DisqualifiedOfficerSearch` | Y           |
| `get_search_dissolved`                | `/dissolved-search/companies`                                                                                    |                             |             |
| `get_search_alphabetical`             | `/alphabetical-search/companies`                                                                                 |                             |             |
| `get_search_advanced`                 | `/advanced-search/companies`                                                                                     |                             |             |


From the [Document API](https://developer-specs.company-information.service.gov.uk/document-api/reference):

- `get_document_metadata` - returns `DocumentMetadata`
- `get_document` - returns a bytes object with the document contents

## Development

### Setup development

### Update constants

```sh
uv run update_ch_enums.py
```