from enum import StrEnum


class ScrapeEnvelopeProxyTier(StrEnum):
    DATACENTER = "datacenter"
    MOBILE = "mobile"
    RESIDENTIAL = "residential"

    def __str__(self) -> str:
        return str(self.value)
