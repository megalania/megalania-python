from enum import StrEnum


class ScrapeProxyTier(StrEnum):
    DATACENTER = "datacenter"
    MOBILE = "mobile"
    RESIDENTIAL = "residential"

    def __str__(self) -> str:
        return str(self.value)
