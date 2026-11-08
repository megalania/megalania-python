from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.geos import Geos
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/geos",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Geos | None:
    if response.status_code == 200:
        response_200 = Geos.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Geos]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Geos]:
    """The countries each route can exit from

     Public and free: no key, no audit row. Each route lists the countries
    its supplier serves, from our configuration, so a country_code it does
    not serve answers 400 on country_code when that route is forced with
    engine or proxy_tier. With engine and proxy_tier left out, we pick
    only routes that serve the country, and a country no route serves
    answers 400 on country_code. A premium country adds its price.

    No error codes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Geos]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> Geos | None:
    """The countries each route can exit from

     Public and free: no key, no audit row. Each route lists the countries
    its supplier serves, from our configuration, so a country_code it does
    not serve answers 400 on country_code when that route is forced with
    engine or proxy_tier. With engine and proxy_tier left out, we pick
    only routes that serve the country, and a country no route serves
    answers 400 on country_code. A premium country adds its price.

    No error codes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Geos
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[Geos]:
    """The countries each route can exit from

     Public and free: no key, no audit row. Each route lists the countries
    its supplier serves, from our configuration, so a country_code it does
    not serve answers 400 on country_code when that route is forced with
    engine or proxy_tier. With engine and proxy_tier left out, we pick
    only routes that serve the country, and a country no route serves
    answers 400 on country_code. A premium country adds its price.

    No error codes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Geos]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> Geos | None:
    """The countries each route can exit from

     Public and free: no key, no audit row. Each route lists the countries
    its supplier serves, from our configuration, so a country_code it does
    not serve answers 400 on country_code when that route is forced with
    engine or proxy_tier. With engine and proxy_tier left out, we pick
    only routes that serve the country, and a country no route serves
    answers 400 on country_code. A premium country adds its price.

    No error codes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Geos
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
