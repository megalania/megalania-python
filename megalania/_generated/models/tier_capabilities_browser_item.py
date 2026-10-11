from enum import StrEnum


class TierCapabilitiesBrowserItem(StrEnum):
    DATACENTER = "datacenter"
    MOBILE = "mobile"
    RESIDENTIAL = "residential"

    def __str__(self) -> str:
        return str(self.value)
