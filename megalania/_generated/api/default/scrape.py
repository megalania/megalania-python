from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.scrape_country_code import ScrapeCountryCode
from ...models.scrape_engine import ScrapeEngine
from ...models.scrape_extract_model import ScrapeExtractModel
from ...models.scrape_identity import ScrapeIdentity
from ...models.scrape_network import ScrapeNetwork
from ...models.scrape_only_main_content import ScrapeOnlyMainContent
from ...models.scrape_proxy_tier import ScrapeProxyTier
from ...models.scrape_response_types_item import ScrapeResponseTypesItem
from ...models.scrape_screenshot import ScrapeScreenshot
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    url_query: str,
    engine: ScrapeEngine | Unset = ScrapeEngine.HTTP,
    country_code: ScrapeCountryCode | Unset = UNSET,
    proxy_city: str | Unset = UNSET,
    proxy_tier: ScrapeProxyTier | Unset = ScrapeProxyTier.RESIDENTIAL,
    identity: ScrapeIdentity | Unset = UNSET,
    session_id: str | Unset = UNSET,
    wait_until: str | Unset = "load",
    response_types: list[ScrapeResponseTypesItem] | Unset = UNSET,
    actions: str | Unset = UNSET,
    screenshot: ScrapeScreenshot | Unset = UNSET,
    network: ScrapeNetwork | Unset = UNSET,
    network_url_globs: str | Unset = UNSET,
    only_main_content: ScrapeOnlyMainContent | Unset = ScrapeOnlyMainContent.TRUE,
    extract: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    prompt: str | Unset = UNSET,
    extract_model: ScrapeExtractModel | Unset = ScrapeExtractModel.DEFAULT,
    headers: list[str] | Unset = UNSET,
    timeout: int | Unset = 60,
    max_credits: int | Unset = UNSET,
    max_age: int | Unset = 300,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    params: dict[str, Any] = {}

    params["url"] = url_query

    json_engine: str | Unset = UNSET
    if not isinstance(engine, Unset):
        json_engine = engine.value

    params["engine"] = json_engine

    json_country_code: str | Unset = UNSET
    if not isinstance(country_code, Unset):
        json_country_code = country_code.value

    params["country_code"] = json_country_code

    params["proxy_city"] = proxy_city

    json_proxy_tier: str | Unset = UNSET
    if not isinstance(proxy_tier, Unset):
        json_proxy_tier = proxy_tier.value

    params["proxy_tier"] = json_proxy_tier

    json_identity: str | Unset = UNSET
    if not isinstance(identity, Unset):
        json_identity = identity.value

    params["identity"] = json_identity

    params["session_id"] = session_id

    params["wait_until"] = wait_until

    json_response_types: list[str] | Unset = UNSET
    if not isinstance(response_types, Unset):
        json_response_types = []
        for response_types_item_data in response_types:
            response_types_item = response_types_item_data.value
            json_response_types.append(response_types_item)

    params["response_types"] = json_response_types

    params["actions"] = actions

    json_screenshot: str | Unset = UNSET
    if not isinstance(screenshot, Unset):
        json_screenshot = screenshot.value

    params["screenshot"] = json_screenshot

    json_network: str | Unset = UNSET
    if not isinstance(network, Unset):
        json_network = network.value

    params["network"] = json_network

    params["network_url_globs"] = network_url_globs

    json_only_main_content: str | Unset = UNSET
    if not isinstance(only_main_content, Unset):
        json_only_main_content = only_main_content.value

    params["only_main_content"] = json_only_main_content

    params["extract"] = extract

    params["schema"] = schema

    params["prompt"] = prompt

    json_extract_model: str | Unset = UNSET
    if not isinstance(extract_model, Unset):
        json_extract_model = extract_model.value

    params["extract_model"] = json_extract_model

    json_headers: list[str] | Unset = UNSET
    if not isinstance(headers, Unset):
        json_headers = headers

    params["headers"] = json_headers

    params["timeout"] = timeout

    params["max_credits"] = max_credits

    params["max_age"] = max_age

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    url_query: str,
    engine: ScrapeEngine | Unset = ScrapeEngine.HTTP,
    country_code: ScrapeCountryCode | Unset = UNSET,
    proxy_city: str | Unset = UNSET,
    proxy_tier: ScrapeProxyTier | Unset = ScrapeProxyTier.RESIDENTIAL,
    identity: ScrapeIdentity | Unset = UNSET,
    session_id: str | Unset = UNSET,
    wait_until: str | Unset = "load",
    response_types: list[ScrapeResponseTypesItem] | Unset = UNSET,
    actions: str | Unset = UNSET,
    screenshot: ScrapeScreenshot | Unset = UNSET,
    network: ScrapeNetwork | Unset = UNSET,
    network_url_globs: str | Unset = UNSET,
    only_main_content: ScrapeOnlyMainContent | Unset = ScrapeOnlyMainContent.TRUE,
    extract: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    prompt: str | Unset = UNSET,
    extract_model: ScrapeExtractModel | Unset = ScrapeExtractModel.DEFAULT,
    headers: list[str] | Unset = UNSET,
    timeout: int | Unset = 60,
    max_credits: int | Unset = UNSET,
    max_age: int | Unset = 300,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | str]:
    """Scrape a URL and stream the result

     Synchronous. The connection stays open until the result streams back
    or the timeout hits. Nothing is buffered; the size cap is 50 MB.
    A target that answers with a status under 500 is a delivered result:
    HTTP 200 from us, the target status in X-Target-Status. Blocks we
    detect are free: a blocked result (401, 403, 407, 429, or a detected
    challenge) costs nothing and is a 422 blocked with X-Billing: blocked
    and no page content. A target 5xx is free too: a 422 target_error with
    the target status in X-Target-Status and no page content.

    Error codes action_failed, bad_extract, bad_parameter, bad_token, blocked, busy, capacity_spent,
    convert_cap, daily_cost_cap, document_unreadable, fetch_error, forbidden_target,
    free_failures_spent, free_tier_cap, idempotency_mismatch, insufficient_credits, internal,
    llm_global_stop, llm_token_cap, llm_unavailable, max_credits_too_low, over_concurrency,
    period_cost_cap, replayed, spend_cap, target_error, target_rate_limited, timeout, unavailable,
    unknown_host, unsupported_content, upstream_cap, wrong_scope.

    Args:
        url_query (str):
        engine (ScrapeEngine | Unset):  Default: ScrapeEngine.HTTP.
        country_code (ScrapeCountryCode | Unset):
        proxy_city (str | Unset):
        proxy_tier (ScrapeProxyTier | Unset):  Default: ScrapeProxyTier.RESIDENTIAL.
        identity (ScrapeIdentity | Unset):
        session_id (str | Unset):
        wait_until (str | Unset):  Default: 'load'.
        response_types (list[ScrapeResponseTypesItem] | Unset):
        actions (str | Unset):
        screenshot (ScrapeScreenshot | Unset):
        network (ScrapeNetwork | Unset):
        network_url_globs (str | Unset):
        only_main_content (ScrapeOnlyMainContent | Unset):  Default: ScrapeOnlyMainContent.TRUE.
        extract (str | Unset):
        schema (str | Unset):
        prompt (str | Unset):
        extract_model (ScrapeExtractModel | Unset):  Default: ScrapeExtractModel.DEFAULT.
        headers (list[str] | Unset):
        timeout (int | Unset):  Default: 60.
        max_credits (int | Unset):
        max_age (int | Unset):  Default: 300.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
    """

    kwargs = _get_kwargs(
        url_query=url_query,
        engine=engine,
        country_code=country_code,
        proxy_city=proxy_city,
        proxy_tier=proxy_tier,
        identity=identity,
        session_id=session_id,
        wait_until=wait_until,
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
        max_credits=max_credits,
        max_age=max_age,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    url_query: str,
    engine: ScrapeEngine | Unset = ScrapeEngine.HTTP,
    country_code: ScrapeCountryCode | Unset = UNSET,
    proxy_city: str | Unset = UNSET,
    proxy_tier: ScrapeProxyTier | Unset = ScrapeProxyTier.RESIDENTIAL,
    identity: ScrapeIdentity | Unset = UNSET,
    session_id: str | Unset = UNSET,
    wait_until: str | Unset = "load",
    response_types: list[ScrapeResponseTypesItem] | Unset = UNSET,
    actions: str | Unset = UNSET,
    screenshot: ScrapeScreenshot | Unset = UNSET,
    network: ScrapeNetwork | Unset = UNSET,
    network_url_globs: str | Unset = UNSET,
    only_main_content: ScrapeOnlyMainContent | Unset = ScrapeOnlyMainContent.TRUE,
    extract: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    prompt: str | Unset = UNSET,
    extract_model: ScrapeExtractModel | Unset = ScrapeExtractModel.DEFAULT,
    headers: list[str] | Unset = UNSET,
    timeout: int | Unset = 60,
    max_credits: int | Unset = UNSET,
    max_age: int | Unset = 300,
    idempotency_key: str | Unset = UNSET,
) -> Error | str | None:
    """Scrape a URL and stream the result

     Synchronous. The connection stays open until the result streams back
    or the timeout hits. Nothing is buffered; the size cap is 50 MB.
    A target that answers with a status under 500 is a delivered result:
    HTTP 200 from us, the target status in X-Target-Status. Blocks we
    detect are free: a blocked result (401, 403, 407, 429, or a detected
    challenge) costs nothing and is a 422 blocked with X-Billing: blocked
    and no page content. A target 5xx is free too: a 422 target_error with
    the target status in X-Target-Status and no page content.

    Error codes action_failed, bad_extract, bad_parameter, bad_token, blocked, busy, capacity_spent,
    convert_cap, daily_cost_cap, document_unreadable, fetch_error, forbidden_target,
    free_failures_spent, free_tier_cap, idempotency_mismatch, insufficient_credits, internal,
    llm_global_stop, llm_token_cap, llm_unavailable, max_credits_too_low, over_concurrency,
    period_cost_cap, replayed, spend_cap, target_error, target_rate_limited, timeout, unavailable,
    unknown_host, unsupported_content, upstream_cap, wrong_scope.

    Args:
        url_query (str):
        engine (ScrapeEngine | Unset):  Default: ScrapeEngine.HTTP.
        country_code (ScrapeCountryCode | Unset):
        proxy_city (str | Unset):
        proxy_tier (ScrapeProxyTier | Unset):  Default: ScrapeProxyTier.RESIDENTIAL.
        identity (ScrapeIdentity | Unset):
        session_id (str | Unset):
        wait_until (str | Unset):  Default: 'load'.
        response_types (list[ScrapeResponseTypesItem] | Unset):
        actions (str | Unset):
        screenshot (ScrapeScreenshot | Unset):
        network (ScrapeNetwork | Unset):
        network_url_globs (str | Unset):
        only_main_content (ScrapeOnlyMainContent | Unset):  Default: ScrapeOnlyMainContent.TRUE.
        extract (str | Unset):
        schema (str | Unset):
        prompt (str | Unset):
        extract_model (ScrapeExtractModel | Unset):  Default: ScrapeExtractModel.DEFAULT.
        headers (list[str] | Unset):
        timeout (int | Unset):  Default: 60.
        max_credits (int | Unset):
        max_age (int | Unset):  Default: 300.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
    """

    return sync_detailed(
        client=client,
        url_query=url_query,
        engine=engine,
        country_code=country_code,
        proxy_city=proxy_city,
        proxy_tier=proxy_tier,
        identity=identity,
        session_id=session_id,
        wait_until=wait_until,
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
        max_credits=max_credits,
        max_age=max_age,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    url_query: str,
    engine: ScrapeEngine | Unset = ScrapeEngine.HTTP,
    country_code: ScrapeCountryCode | Unset = UNSET,
    proxy_city: str | Unset = UNSET,
    proxy_tier: ScrapeProxyTier | Unset = ScrapeProxyTier.RESIDENTIAL,
    identity: ScrapeIdentity | Unset = UNSET,
    session_id: str | Unset = UNSET,
    wait_until: str | Unset = "load",
    response_types: list[ScrapeResponseTypesItem] | Unset = UNSET,
    actions: str | Unset = UNSET,
    screenshot: ScrapeScreenshot | Unset = UNSET,
    network: ScrapeNetwork | Unset = UNSET,
    network_url_globs: str | Unset = UNSET,
    only_main_content: ScrapeOnlyMainContent | Unset = ScrapeOnlyMainContent.TRUE,
    extract: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    prompt: str | Unset = UNSET,
    extract_model: ScrapeExtractModel | Unset = ScrapeExtractModel.DEFAULT,
    headers: list[str] | Unset = UNSET,
    timeout: int | Unset = 60,
    max_credits: int | Unset = UNSET,
    max_age: int | Unset = 300,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | str]:
    """Scrape a URL and stream the result

     Synchronous. The connection stays open until the result streams back
    or the timeout hits. Nothing is buffered; the size cap is 50 MB.
    A target that answers with a status under 500 is a delivered result:
    HTTP 200 from us, the target status in X-Target-Status. Blocks we
    detect are free: a blocked result (401, 403, 407, 429, or a detected
    challenge) costs nothing and is a 422 blocked with X-Billing: blocked
    and no page content. A target 5xx is free too: a 422 target_error with
    the target status in X-Target-Status and no page content.

    Error codes action_failed, bad_extract, bad_parameter, bad_token, blocked, busy, capacity_spent,
    convert_cap, daily_cost_cap, document_unreadable, fetch_error, forbidden_target,
    free_failures_spent, free_tier_cap, idempotency_mismatch, insufficient_credits, internal,
    llm_global_stop, llm_token_cap, llm_unavailable, max_credits_too_low, over_concurrency,
    period_cost_cap, replayed, spend_cap, target_error, target_rate_limited, timeout, unavailable,
    unknown_host, unsupported_content, upstream_cap, wrong_scope.

    Args:
        url_query (str):
        engine (ScrapeEngine | Unset):  Default: ScrapeEngine.HTTP.
        country_code (ScrapeCountryCode | Unset):
        proxy_city (str | Unset):
        proxy_tier (ScrapeProxyTier | Unset):  Default: ScrapeProxyTier.RESIDENTIAL.
        identity (ScrapeIdentity | Unset):
        session_id (str | Unset):
        wait_until (str | Unset):  Default: 'load'.
        response_types (list[ScrapeResponseTypesItem] | Unset):
        actions (str | Unset):
        screenshot (ScrapeScreenshot | Unset):
        network (ScrapeNetwork | Unset):
        network_url_globs (str | Unset):
        only_main_content (ScrapeOnlyMainContent | Unset):  Default: ScrapeOnlyMainContent.TRUE.
        extract (str | Unset):
        schema (str | Unset):
        prompt (str | Unset):
        extract_model (ScrapeExtractModel | Unset):  Default: ScrapeExtractModel.DEFAULT.
        headers (list[str] | Unset):
        timeout (int | Unset):  Default: 60.
        max_credits (int | Unset):
        max_age (int | Unset):  Default: 300.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
    """

    kwargs = _get_kwargs(
        url_query=url_query,
        engine=engine,
        country_code=country_code,
        proxy_city=proxy_city,
        proxy_tier=proxy_tier,
        identity=identity,
        session_id=session_id,
        wait_until=wait_until,
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
        max_credits=max_credits,
        max_age=max_age,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    url_query: str,
    engine: ScrapeEngine | Unset = ScrapeEngine.HTTP,
    country_code: ScrapeCountryCode | Unset = UNSET,
    proxy_city: str | Unset = UNSET,
    proxy_tier: ScrapeProxyTier | Unset = ScrapeProxyTier.RESIDENTIAL,
    identity: ScrapeIdentity | Unset = UNSET,
    session_id: str | Unset = UNSET,
    wait_until: str | Unset = "load",
    response_types: list[ScrapeResponseTypesItem] | Unset = UNSET,
    actions: str | Unset = UNSET,
    screenshot: ScrapeScreenshot | Unset = UNSET,
    network: ScrapeNetwork | Unset = UNSET,
    network_url_globs: str | Unset = UNSET,
    only_main_content: ScrapeOnlyMainContent | Unset = ScrapeOnlyMainContent.TRUE,
    extract: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    prompt: str | Unset = UNSET,
    extract_model: ScrapeExtractModel | Unset = ScrapeExtractModel.DEFAULT,
    headers: list[str] | Unset = UNSET,
    timeout: int | Unset = 60,
    max_credits: int | Unset = UNSET,
    max_age: int | Unset = 300,
    idempotency_key: str | Unset = UNSET,
) -> Error | str | None:
    """Scrape a URL and stream the result

     Synchronous. The connection stays open until the result streams back
    or the timeout hits. Nothing is buffered; the size cap is 50 MB.
    A target that answers with a status under 500 is a delivered result:
    HTTP 200 from us, the target status in X-Target-Status. Blocks we
    detect are free: a blocked result (401, 403, 407, 429, or a detected
    challenge) costs nothing and is a 422 blocked with X-Billing: blocked
    and no page content. A target 5xx is free too: a 422 target_error with
    the target status in X-Target-Status and no page content.

    Error codes action_failed, bad_extract, bad_parameter, bad_token, blocked, busy, capacity_spent,
    convert_cap, daily_cost_cap, document_unreadable, fetch_error, forbidden_target,
    free_failures_spent, free_tier_cap, idempotency_mismatch, insufficient_credits, internal,
    llm_global_stop, llm_token_cap, llm_unavailable, max_credits_too_low, over_concurrency,
    period_cost_cap, replayed, spend_cap, target_error, target_rate_limited, timeout, unavailable,
    unknown_host, unsupported_content, upstream_cap, wrong_scope.

    Args:
        url_query (str):
        engine (ScrapeEngine | Unset):  Default: ScrapeEngine.HTTP.
        country_code (ScrapeCountryCode | Unset):
        proxy_city (str | Unset):
        proxy_tier (ScrapeProxyTier | Unset):  Default: ScrapeProxyTier.RESIDENTIAL.
        identity (ScrapeIdentity | Unset):
        session_id (str | Unset):
        wait_until (str | Unset):  Default: 'load'.
        response_types (list[ScrapeResponseTypesItem] | Unset):
        actions (str | Unset):
        screenshot (ScrapeScreenshot | Unset):
        network (ScrapeNetwork | Unset):
        network_url_globs (str | Unset):
        only_main_content (ScrapeOnlyMainContent | Unset):  Default: ScrapeOnlyMainContent.TRUE.
        extract (str | Unset):
        schema (str | Unset):
        prompt (str | Unset):
        extract_model (ScrapeExtractModel | Unset):  Default: ScrapeExtractModel.DEFAULT.
        headers (list[str] | Unset):
        timeout (int | Unset):  Default: 60.
        max_credits (int | Unset):
        max_age (int | Unset):  Default: 300.
        idempotency_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
    """

    return (
        await asyncio_detailed(
            client=client,
            url_query=url_query,
            engine=engine,
            country_code=country_code,
            proxy_city=proxy_city,
            proxy_tier=proxy_tier,
            identity=identity,
            session_id=session_id,
            wait_until=wait_until,
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
            max_credits=max_credits,
            max_age=max_age,
            idempotency_key=idempotency_key,
        )
    ).parsed
