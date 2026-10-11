from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.map_request import MapRequest
from ...models.map_result import MapResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: MapRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/map",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | MapResult | None:
    if response.status_code == 200:
        response_200 = MapResult.from_dict(response.json())

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

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
) -> Response[Error | MapResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MapRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | MapResult]:
    """List a site's URLs without fetching their content

     Reads the site's robots.txt, the sitemaps it names (or /sitemap.xml),
    at most 10 sitemap files, gzipped ones included, and the same-host
    links on the start page: at most 12 fetches, on the one route the
    first fetch picks. Each URL says where it came from. truncated is true
    when the limit, the route's byte cap or your balance stopped the map
    early. A map costs 4 credits with 512 KiB of wire on HTTP datacenter;
    above that, and on a residential or browser route, the route's normal
    byte and rung prices apply to every byte of every fetch. A map where
    we could not read the site (blocked or failed fetches) is free; a search
    that matches nothing is still charged. The URLs go to you only and are never stored.

    Args:
        idempotency_key (str | Unset):
        body (MapRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MapResult]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: MapRequest,
    idempotency_key: str | Unset = UNSET,
) -> Error | MapResult | None:
    """List a site's URLs without fetching their content

     Reads the site's robots.txt, the sitemaps it names (or /sitemap.xml),
    at most 10 sitemap files, gzipped ones included, and the same-host
    links on the start page: at most 12 fetches, on the one route the
    first fetch picks. Each URL says where it came from. truncated is true
    when the limit, the route's byte cap or your balance stopped the map
    early. A map costs 4 credits with 512 KiB of wire on HTTP datacenter;
    above that, and on a residential or browser route, the route's normal
    byte and rung prices apply to every byte of every fetch. A map where
    we could not read the site (blocked or failed fetches) is free; a search
    that matches nothing is still charged. The URLs go to you only and are never stored.

    Args:
        idempotency_key (str | Unset):
        body (MapRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MapResult
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MapRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | MapResult]:
    """List a site's URLs without fetching their content

     Reads the site's robots.txt, the sitemaps it names (or /sitemap.xml),
    at most 10 sitemap files, gzipped ones included, and the same-host
    links on the start page: at most 12 fetches, on the one route the
    first fetch picks. Each URL says where it came from. truncated is true
    when the limit, the route's byte cap or your balance stopped the map
    early. A map costs 4 credits with 512 KiB of wire on HTTP datacenter;
    above that, and on a residential or browser route, the route's normal
    byte and rung prices apply to every byte of every fetch. A map where
    we could not read the site (blocked or failed fetches) is free; a search
    that matches nothing is still charged. The URLs go to you only and are never stored.

    Args:
        idempotency_key (str | Unset):
        body (MapRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MapResult]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: MapRequest,
    idempotency_key: str | Unset = UNSET,
) -> Error | MapResult | None:
    """List a site's URLs without fetching their content

     Reads the site's robots.txt, the sitemaps it names (or /sitemap.xml),
    at most 10 sitemap files, gzipped ones included, and the same-host
    links on the start page: at most 12 fetches, on the one route the
    first fetch picks. Each URL says where it came from. truncated is true
    when the limit, the route's byte cap or your balance stopped the map
    early. A map costs 4 credits with 512 KiB of wire on HTTP datacenter;
    above that, and on a residential or browser route, the route's normal
    byte and rung prices apply to every byte of every fetch. A map where
    we could not read the site (blocked or failed fetches) is free; a search
    that matches nothing is still charged. The URLs go to you only and are never stored.

    Args:
        idempotency_key (str | Unset):
        body (MapRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MapResult
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
