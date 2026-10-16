from enum import StrEnum


class DescriptionIdentifier(StrEnum):
    ADMINISTRATION = "administration"
    APPOINTMENT_COUNT = "appointment-count"
    BORN_ON = "born-on"
    CLOSED = "closed"
    CLOSED_ON = "closed-on"
    CONVERTED_CLOSED_ON = "converted-closed-on"
    DISSOLVED_ON = "dissolved-on"
    FIRST_UK_ESTABLISHMENT_OPENED_ON = "first-uk-establishment-opened-on"
    FORMED_ON = "formed-on"
    INCORPORATED_ON = "incorporated-on"
    INSOLVENCY_PROCEEDINGS = "insolvency-proceedings"
    LIQUIDATION = "liquidation"
    NOTIFICATION_COUNT = "notification-count"
    OPENED_ON = "opened-on"
    RECEIVERSHIP = "receivership"
    REGISTERED = "registered"
    REGISTERED_ON = "registered-on"
    REMOVED = "removed"
    VOLUNTARY_ARRANGEMENT = "voluntary-arrangement"


class Country(StrEnum):
    WALES = "Wales"
    ENGLAND = "England"
    SCOTLAND = "Scotland"
    GREAT_BRITAIN = "Great Britain"
    NOT_SPECIFIED = "Not specified"
    UNITED_KINGDOM = "United Kingdom"
    NORTHERN_IRELAND = "Northern Ireland"


class ResponseKind(StrEnum):
    FILING_HISTORY = "filing-history"
    OFFICER_LIST = "officer-list"
    REGISTERED_OFFICE_ADDRESS = "registered-office-address"
    REGISTERS = "registers"
    SEARCH_ALL = "search#all"
    SEARCH_ADVANCEDSEARCH = "search#advanced-search"
    SEARCH_ALPHABETICALDISSOLVED = "search#alphabetical-dissolved"
    SEARCH_ALPHABETICALSEARCH = "search#alphabetical-search"
    SEARCH_COMPANIES = "search#companies"
    SEARCH_DISQUALIFIEDOFFICER = "search#disqualified-officers"
    SEARCH_DISSOLVED = "search#dissolved"
    SEARCH_ENHANCEDSEARCH = "search#enhanced-search"
    SEARCH_OFFICERS = "search#officers"
    SEARCH_PERSONSWITHSIGNIFICANTCONTROL = "search#persons-with-significant-control"
    SEARCH_PREVIOUSNAMEDISSOLVED = "search#previous-name-dissolved"
    SEARCHRESULTS_ALPHABETICALSEARCH = "searchresults#alphabetical-search"
    SEARCHRESULTS_COMPANY = "searchresults#company"
    SEARCH_RESULTS_COMPANY = "search-results#company"
    SEARCHRESULTS_DISQUALIFIEDOFFICER = "searchresults#disqualified-officer"
    SEARCHRESULTS_DISSOLVEDCOMPANY = "searchresults#dissolved-company"
    SEARCHRESULTS_OFFICER = "searchresults#officer"
    SEARCHRESULTS_PERSONSWITHSIGNIFICANTCONTROL = (
        "searchresults#persons-with-significant-control"
    )
