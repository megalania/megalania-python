from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..models.scrape_envelope_country_code import ScrapeEnvelopeCountryCode
from ..models.scrape_envelope_engine import ScrapeEnvelopeEngine
from ..models.scrape_envelope_extract_model import ScrapeEnvelopeExtractModel
from ..models.scrape_envelope_identity import ScrapeEnvelopeIdentity
from ..models.scrape_envelope_method import ScrapeEnvelopeMethod
from ..models.scrape_envelope_only_main_content import ScrapeEnvelopeOnlyMainContent
from ..models.scrape_envelope_proxy_tier import ScrapeEnvelopeProxyTier
from ..models.scrape_envelope_screenshot import ScrapeEnvelopeScreenshot
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScrapeEnvelope")


@_attrs_define
class ScrapeEnvelope:
    """The POST /v1 request body. Every value is a string, except headers, which is a list of strings. An unknown key is a
    400.

        Attributes:
            url (str): Absolute http(s) URL to scrape, sent as it is. Nothing of ours is in the query string on this route,
                so the target's own query needs no encoding.
            method (ScrapeEnvelopeMethod | Unset): The method sent to the target. POST is the one that may carry body and
                content_type. Default: ScrapeEnvelopeMethod.GET.
            body (str | Unset): The target request body, base64. Only with method POST.
            content_type (str | Unset): Media type of body, for example application/json. Only with method POST.
            engine (ScrapeEnvelopeEngine | Unset): Which engine fetches the page. Leave it out and we pick. http sends one
                plain request. browser renders the page in Chrome on a datacenter exit, GET only. Default:
                ScrapeEnvelopeEngine.HTTP.
            country_code (ScrapeEnvelopeCountryCode | Unset): Exit country, ISO 3166-1 alpha-2. Default is the platform's
                configured country.
            proxy_city (str | Unset): Exit city in the proxy provider's spelling, for example new_york.
            proxy_tier (ScrapeEnvelopeProxyTier | Unset): Which proxy pool the request leaves from. Cheaper pools are
                blocked more often. Default: ScrapeEnvelopeProxyTier.RESIDENTIAL.
            identity (ScrapeEnvelopeIdentity | Unset): Which browser the fetch looks like on the wire. Leave it out and we
                pick.
            session_id (str | Unset): Send the same value again to leave from the same IP. 1 to 64 letters, digits, - or _.
                Your sessions are yours alone.
            response_types (str | Unset): Comma-separated list of html, json, markdown, text, links, metadata, page_data,
                compact_html. Several means multipart/mixed, one part per type, in request order. Default: 'html'.
            actions (str | Unset): Same rule as the query parameter. The recommended way to send type, so the text is not in
                a URL.
            screenshot (ScrapeEnvelopeScreenshot | Unset): Same rule as the query parameter. A JPEG link in a part named
                screenshot.
            network (bool | Unset): Same rule as the query parameter. The page's XHR and fetch responses in a part named
                network.
            network_url_globs (str | Unset): Same rule as the query parameter.
            only_main_content (ScrapeEnvelopeOnlyMainContent | Unset): Same rule as the query parameter. false returns the
                whole page and needs markdown, text or compact_html in response_types. Default:
                ScrapeEnvelopeOnlyMainContent.TRUE.
            extract (str | Unset): Selector rules, required with response_types=json and only valid with it. <name>:<css>
                joined by |, at most 32 rules and 4096 bytes. Add @attr to read an attribute instead of the text, and a trailing
                * to get a list. The answer is bounded: 8 MB in total, 1000 matches for one list rule, 1 MB for one value. A
                rule that reaches a bound stops there and the object gains truncated: true. That is a delivered result and is
                charged, so truncated is the one name a rule cannot have. Example: title:h1|links:a@href*
            schema (str | Unset): Same rule as the query parameter, as a JSON string.
            prompt (str | Unset): Same rule as the query parameter.
            extract_model (ScrapeEnvelopeExtractModel | Unset): Same rule as the query parameter.
            headers (list[str] | Unset): Extra request headers, each as name:value.
            timeout (str | Unset): Seconds to wait for the result, 1 to 90. Default: '60'.
            cost_budget (str | Unset): The most credits this request may cost, 1 to 32767. A budget below the price is a 400
                naming cost_budget.
            max_credits (str | Unset): The most credits one page may cost, 1 to 32767. Routes priced above it are left out;
                if none is left, a free 400 max_credits_too_low.
    """

    url: str
    method: ScrapeEnvelopeMethod | Unset = ScrapeEnvelopeMethod.GET
    body: str | Unset = UNSET
    content_type: str | Unset = UNSET
    engine: ScrapeEnvelopeEngine | Unset = ScrapeEnvelopeEngine.HTTP
    country_code: ScrapeEnvelopeCountryCode | Unset = UNSET
    proxy_city: str | Unset = UNSET
    proxy_tier: ScrapeEnvelopeProxyTier | Unset = ScrapeEnvelopeProxyTier.RESIDENTIAL
    identity: ScrapeEnvelopeIdentity | Unset = UNSET
    session_id: str | Unset = UNSET
    response_types: str | Unset = "html"
    actions: str | Unset = UNSET
    screenshot: ScrapeEnvelopeScreenshot | Unset = UNSET
    network: bool | Unset = UNSET
    network_url_globs: str | Unset = UNSET
    only_main_content: ScrapeEnvelopeOnlyMainContent | Unset = (
        ScrapeEnvelopeOnlyMainContent.TRUE
    )
    extract: str | Unset = UNSET
    schema: str | Unset = UNSET
    prompt: str | Unset = UNSET
    extract_model: ScrapeEnvelopeExtractModel | Unset = UNSET
    headers: list[str] | Unset = UNSET
    timeout: str | Unset = "60"
    cost_budget: str | Unset = UNSET
    max_credits: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        method: str | Unset = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        body = self.body

        content_type = self.content_type

        engine: str | Unset = UNSET
        if not isinstance(self.engine, Unset):
            engine = self.engine.value

        country_code: str | Unset = UNSET
        if not isinstance(self.country_code, Unset):
            country_code = self.country_code.value

        proxy_city = self.proxy_city

        proxy_tier: str | Unset = UNSET
        if not isinstance(self.proxy_tier, Unset):
            proxy_tier = self.proxy_tier.value

        identity: str | Unset = UNSET
        if not isinstance(self.identity, Unset):
            identity = self.identity.value

        session_id = self.session_id

        response_types = self.response_types

        actions = self.actions

        screenshot: str | Unset = UNSET
        if not isinstance(self.screenshot, Unset):
            screenshot = self.screenshot.value

        network = self.network

        network_url_globs = self.network_url_globs

        only_main_content: str | Unset = UNSET
        if not isinstance(self.only_main_content, Unset):
            only_main_content = self.only_main_content.value

        extract = self.extract

        schema = self.schema

        prompt = self.prompt

        extract_model: str | Unset = UNSET
        if not isinstance(self.extract_model, Unset):
            extract_model = self.extract_model.value

        headers: list[str] | Unset = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers

        timeout = self.timeout

        cost_budget = self.cost_budget

        max_credits = self.max_credits

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method
        if body is not UNSET:
            field_dict["body"] = body
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if engine is not UNSET:
            field_dict["engine"] = engine
        if country_code is not UNSET:
            field_dict["country_code"] = country_code
        if proxy_city is not UNSET:
            field_dict["proxy_city"] = proxy_city
        if proxy_tier is not UNSET:
            field_dict["proxy_tier"] = proxy_tier
        if identity is not UNSET:
            field_dict["identity"] = identity
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if response_types is not UNSET:
            field_dict["response_types"] = response_types
        if actions is not UNSET:
            field_dict["actions"] = actions
        if screenshot is not UNSET:
            field_dict["screenshot"] = screenshot
        if network is not UNSET:
            field_dict["network"] = network
        if network_url_globs is not UNSET:
            field_dict["network_url_globs"] = network_url_globs
        if only_main_content is not UNSET:
            field_dict["only_main_content"] = only_main_content
        if extract is not UNSET:
            field_dict["extract"] = extract
        if schema is not UNSET:
            field_dict["schema"] = schema
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if extract_model is not UNSET:
            field_dict["extract_model"] = extract_model
        if headers is not UNSET:
            field_dict["headers"] = headers
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if cost_budget is not UNSET:
            field_dict["cost_budget"] = cost_budget
        if max_credits is not UNSET:
            field_dict["max_credits"] = max_credits

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        url = d.pop("url")

        _method = d.pop("method", UNSET)
        method: ScrapeEnvelopeMethod | Unset
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = ScrapeEnvelopeMethod(_method)

        body = d.pop("body", UNSET)

        content_type = d.pop("content_type", UNSET)

        _engine = d.pop("engine", UNSET)
        engine: ScrapeEnvelopeEngine | Unset
        if isinstance(_engine, Unset):
            engine = UNSET
        else:
            engine = ScrapeEnvelopeEngine(_engine)

        _country_code = d.pop("country_code", UNSET)
        country_code: ScrapeEnvelopeCountryCode | Unset
        if isinstance(_country_code, Unset):
            country_code = UNSET
        else:
            country_code = ScrapeEnvelopeCountryCode(_country_code)

        proxy_city = d.pop("proxy_city", UNSET)

        _proxy_tier = d.pop("proxy_tier", UNSET)
        proxy_tier: ScrapeEnvelopeProxyTier | Unset
        if isinstance(_proxy_tier, Unset):
            proxy_tier = UNSET
        else:
            proxy_tier = ScrapeEnvelopeProxyTier(_proxy_tier)

        _identity = d.pop("identity", UNSET)
        identity: ScrapeEnvelopeIdentity | Unset
        if isinstance(_identity, Unset):
            identity = UNSET
        else:
            identity = ScrapeEnvelopeIdentity(_identity)

        session_id = d.pop("session_id", UNSET)

        response_types = d.pop("response_types", UNSET)

        actions = d.pop("actions", UNSET)

        _screenshot = d.pop("screenshot", UNSET)
        screenshot: ScrapeEnvelopeScreenshot | Unset
        if isinstance(_screenshot, Unset):
            screenshot = UNSET
        else:
            screenshot = ScrapeEnvelopeScreenshot(_screenshot)

        network = d.pop("network", UNSET)

        network_url_globs = d.pop("network_url_globs", UNSET)

        _only_main_content = d.pop("only_main_content", UNSET)
        only_main_content: ScrapeEnvelopeOnlyMainContent | Unset
        if isinstance(_only_main_content, Unset):
            only_main_content = UNSET
        else:
            only_main_content = ScrapeEnvelopeOnlyMainContent(_only_main_content)

        extract = d.pop("extract", UNSET)

        schema = d.pop("schema", UNSET)

        prompt = d.pop("prompt", UNSET)

        _extract_model = d.pop("extract_model", UNSET)
        extract_model: ScrapeEnvelopeExtractModel | Unset
        if isinstance(_extract_model, Unset):
            extract_model = UNSET
        else:
            extract_model = ScrapeEnvelopeExtractModel(_extract_model)

        headers = cast(list[str], d.pop("headers", UNSET))

        timeout = d.pop("timeout", UNSET)

        cost_budget = d.pop("cost_budget", UNSET)

        max_credits = d.pop("max_credits", UNSET)

        scrape_envelope = cls(
            url=url,
            method=method,
            body=body,
            content_type=content_type,
            engine=engine,
            country_code=country_code,
            proxy_city=proxy_city,
            proxy_tier=proxy_tier,
            identity=identity,
            session_id=session_id,
            response_types=response_types,
            actions=actions,
            screenshot=screenshot,
            network=network,
            network_url_globs=network_url_globs,
            only_main_content=only_main_content,
            extract=extract,
            schema=schema,
            prompt=prompt,
            extract_model=extract_model,
            headers=headers,
            timeout=timeout,
            cost_budget=cost_budget,
            max_credits=max_credits,
        )

        scrape_envelope.additional_properties = d
        return scrape_envelope

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
