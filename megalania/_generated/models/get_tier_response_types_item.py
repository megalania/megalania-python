from enum import StrEnum


class GetTierResponseTypesItem(StrEnum):
    COMPACT_HTML = "compact_html"
    HTML = "html"
    JSON = "json"
    LINKS = "links"
    MARKDOWN = "markdown"
    METADATA = "metadata"
    PAGE_DATA = "page_data"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
