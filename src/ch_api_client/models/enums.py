from enum import StrEnum


class DescriptionIdentifier(StrEnum):
    INCORPORATED_ON = "incorporated-on"
    REGISTERED_ON = "registered-on"
    FORMED_ON = "formed-on"
    DISSOLVED_ON = "dissolved-on"
    CONVERTED_CLOSED_ON = "converted-closed-on"
    CLOSED_ON = "closed-on"
    CLOSED = "closed"
    FIRST_UK_ESTABLISHMENT_OPENED_ON = "first-uk-establishment-opened-on"
    OPENED_ON = "opened-on"
    VOLUNTARY_ARRANGEMENT = "voluntary-arrangement"
    RECEIVERSHIP = "receivership"
    INSOLVENCY_PROCEEDINGS = "insolvency-proceedings"
    LIQUIDATION = "liquidation"
    ADMINISTRATION = "administration"
    APPOINTMENT_COUNT = "appointment-count"
    BORN_ON = "born-on"
    REGISTERED = "registered"
    REMOVED = "removed"
    NOTIFICATION_COUNT = "notification-count"


class Country(StrEnum):
    WALES = "Wales"
    ENGLAND = "England"
    SCOTLAND = "Scotland"
    GREAT_BRITAIN = "Great Britain"
    NOT_SPECIFIED = "Not specified"
    UNITED_KINGDOM = "United Kingdom"
    NORTHERN_IRELAND = "Northern Ireland"


class ResponseKind(StrEnum):
    SEARCH_ALL = "search#all"
    SEARCH_COMPANIES = "search#companies"
    SEARCH_PERSONSWITHSIGNIFICANTCONTROL = "search#persons-with-significant-control"
    SEARCH_OFFICERS = "search#officers"
    SEARCH_DISQUALIFIEDOFFICER = "search#disqualified-officers"
    SEARCHRESULTS_COMPANY = "searchresults#company"
    SEARCHRESULTS_OFFICER = "searchresults#officer"
    SEARCHRESULTS_PERSONSWITHSIGNIFICANTCONTROL = (
        "searchresults#persons-with-significant-control"
    )
    SEARCHRESULTS_DISQUALIFIEDOFFICER = "searchresults#disqualified-officer"
    OFFICER_LIST = "officer-list"
    FILING_HISTORY = "filing-history"
    REGISTERED_OFFICE_ADDRESS = "registered-office-address"
