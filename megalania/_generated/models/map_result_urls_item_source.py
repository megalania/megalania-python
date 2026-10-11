from enum import StrEnum


class MapResultUrlsItemSource(StrEnum):
    LINK = "link"
    SITEMAP = "sitemap"

    def __str__(self) -> str:
        return str(self.value)
