from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_tier_country_code import GetTierCountryCode
from ...models.get_tier_response_types_item import GetTierResponseTypesItem
from ...models.tier import Tier
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    host: str,
    country_code: GetTierCountryCode | Unset = UNSET,
    response_types: list[GetTierResponseTypesItem] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["host"] = host

    json_country_code: str | Unset = UNSET
    if not isinstance(country_code, Unset):
        json_country_code = country_code.value

    params["country_code"] = json_country_code

    json_response_types: list[str] | Unset = UNSET
    if not isinstance(response_types, Unset):
        json_response_types = []
        for response_types_item_data in response_types:
            response_types_item = response_types_item_data.value
            json_response_types.append(response_types_item)

    params["response_types"] = json_response_types

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tier",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Tier | None:
    if response.status_code == 200:
        response_200 = Tier.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

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
) -> Response[Error | Tier]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    host: str,
    country_code: GetTierCountryCode | Unset = UNSET,
    response_types: list[GetTierResponseTypesItem] | Unset = UNSET,
) -> Response[Error | Tier]:
    """The price tier of one host, and what each route to it costs

     Free, and writes no audit row. It shares your plan's concurrency limit
    with /v1. A host with no tier in effect yet answers tier, temporary,
    price and pending as null.

    Error codes bad_parameter, bad_token, busy, internal, over_concurrency, wrong_scope.

    Args:
        host (str):
        country_code (GetTierCountryCode | Unset):
        response_types (list[GetTierResponseTypesItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Tier]
    """

    kwargs = _get_kwargs(
        host=host,
        country_code=country_code,
        response_types=response_types,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    host: str,
    country_code: GetTierCountryCode | Unset = UNSET,
    response_types: list[GetTierResponseTypesItem] | Unset = UNSET,
) -> Error | Tier | None:
    """The price tier of one host, and what each route to it costs

     Free, and writes no audit row. It shares your plan's concurrency limit
    with /v1. A host with no tier in effect yet answers tier, temporary,
    price and pending as null.

    Error codes bad_parameter, bad_token, busy, internal, over_concurrency, wrong_scope.

    Args:
        host (str):
        country_code (GetTierCountryCode | Unset):
        response_types (list[GetTierResponseTypesItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Tier
    """

    return sync_detailed(
        client=client,
        host=host,
        country_code=country_code,
        response_types=response_types,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    host: str,
    country_code: GetTierCountryCode | Unset = UNSET,
    response_types: list[GetTierResponseTypesItem] | Unset = UNSET,
) -> Response[Error | Tier]:
    """The price tier of one host, and what each route to it costs

     Free, and writes no audit row. It shares your plan's concurrency limit
    with /v1. A host with no tier in effect yet answers tier, temporary,
    price and pending as null.

    Error codes bad_parameter, bad_token, busy, internal, over_concurrency, wrong_scope.

    Args:
        host (str):
        country_code (GetTierCountryCode | Unset):
        response_types (list[GetTierResponseTypesItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Tier]
    """

    kwargs = _get_kwargs(
        host=host,
        country_code=country_code,
        response_types=response_types,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    host: str,
    country_code: GetTierCountryCode | Unset = UNSET,
    response_types: list[GetTierResponseTypesItem] | Unset = UNSET,
) -> Error | Tier | None:
    """The price tier of one host, and what each route to it costs

     Free, and writes no audit row. It shares your plan's concurrency limit
    with /v1. A host with no tier in effect yet answers tier, temporary,
    price and pending as null.

    Error codes bad_parameter, bad_token, busy, internal, over_concurrency, wrong_scope.

    Args:
        host (str):
        country_code (GetTierCountryCode | Unset):
        response_types (list[GetTierResponseTypesItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Tier
    """

    return (
        await asyncio_detailed(
            client=client,
            host=host,
            country_code=country_code,
            response_types=response_types,
        )
    ).parsed
