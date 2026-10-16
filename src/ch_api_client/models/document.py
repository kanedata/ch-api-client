import dataclasses
import datetime as dt
from enum import StrEnum

from pydantic.dataclasses import dataclass


class ContentType(StrEnum):
    PDF = "application/pdf"
    JSON = "application/json"
    XML = "application/xml"
    XHTML = "application/xhtml+xml"
    ZIP = "application/zip"
    CSV = "text/csv"


@dataclass
class Resource:
    content_length: int | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The size of the document when returned as this content-type."
        },
    )
    created_at: dt.datetime | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date and time this document type was first created"
        },
    )
    updated_at: dt.datetime | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The date and time the document type was last updated"
        },
    )


@dataclass
class DocumentMetadataLinks:
    self: str | None = dataclasses.field(
        default=None,
        metadata={"description": "Link to this document."},
    )
    document: str | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Link to the document metadata associated with this document."
        },
    )


@dataclass
class DocumentMetadata:
    created_at: dt.datetime | None = dataclasses.field(
        default=None,
        metadata={"description": "The date and time the document was first created"},
    )
    etag: str | None = dataclasses.field(
        default=None, metadata={"description": "The ETag of the resource."}
    )
    links: DocumentMetadataLinks | None = dataclasses.field(
        default=None,
        metadata={
            "description": "Links to other resources associated with this filing history item."
        },
    )
    id: str | None = dataclasses.field(
        default=None, metadata={"description": "The document ID."}
    )
    pages: int | None = dataclasses.field(
        default=None, metadata={"description": "The document page count"}
    )
    resources: dict[ContentType, Resource] | None = dataclasses.field(
        default=None,
        metadata={
            "description": "The list of content-types that the document is available as, and associated type specific information"
        },
    )
    updated_at: dt.datetime | None = dataclasses.field(
        default=None,
        metadata={"description": "The date and time the document was last updated"},
    )

    @property
    def document_id(self):
        if self.id is not None:
            return self.id
        if self.links and self.links.self:
            return self.links.self.split("/")[-1]
        return None

    @property
    def has_ixbrl(self):
        return bool(
            self.resources
            and (
                ContentType.XHTML in self.resources or ContentType.XML in self.resources
            )
        )

    @property
    def has_pdf(self):
        return bool(self.resources and ContentType.PDF in self.resources)
