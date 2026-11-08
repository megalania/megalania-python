from typing import Any

from llama_index.core.bridge.pydantic import Field, SecretStr
from llama_index.core.readers.base import BasePydanticReader
from llama_index.core.schema import Document
from megalania import Megalania


class MegalaniaReader(BasePydanticReader):
    api_key: SecretStr | None = Field(default=None, exclude=True, repr=False)
    continue_on_failure: bool = False
    base_url: str = "https://get.megalania.io"
    api_url: str = "https://api.megalania.io"
    is_remote: bool = True

    @classmethod
    def class_name(cls) -> str:
        return "MegalaniaReader"

    def load_data(self, urls: str | list[str], crawl: dict | None = None, **params: Any) -> list[Document]:
        key = self.api_key.get_secret_value() if self.api_key else None
        with Megalania(key, base_url=self.base_url, api_url=self.api_url) as meg:
            return [Document(text=text, metadata=meta) for text, meta in
                    meg.read_pages(urls, crawl=crawl, continue_on_failure=self.continue_on_failure, **params)]


__all__ = ["MegalaniaReader"]
