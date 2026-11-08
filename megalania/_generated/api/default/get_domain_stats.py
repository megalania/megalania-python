from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.domain_stats import DomainStats
from ...models.error import Error
from ...models.get_domain_stats_days import GetDomainStatsDays
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    host: str,
    days: GetDomainStatsDays | Unset = GetDomainStatsDays.VALUE_7,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["host"] = host

    json_days: int | Unset = UNSET
    if not isinstance(days, Unset):
        json_days = days.value

    params["days"] = json_days

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/stats/domain",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DomainStats | Error | None:
    if response.status_code == 200:
        response_200 = DomainStats.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DomainStats | Error]:
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
    days: GetDomainStatsDays | Unset = GetDomainStatsDays.VALUE_7,
) -> Response[DomainStats | Error]:
    """How the whole platform does on one host

     Free. The numbers are the whole platform's, per host: shop.example.com
    and example.com are two answers, and www. is dropped. They are rolled
    up every hour, at 20 minutes past, so a fetch shows within about 80
    minutes, today included. Only fetches that reached the site count:
    refusals before the fetch (balance, limits, capacity) are left out. A
    breakdown line is shown only when at least 3 customers and at least
    20 requests are behind it in the window, and requests counts only
    the lines shown; with no line left the answer is requests 0 and an
    empty breakdown. Customers are counted per day, so a line whose
    customers came on different days can stay hidden. The answer is
    cached for five minutes.

    Error codes bad_parameter, bad_token, internal, wrong_scope.

    Args:
        host (str):
        days (GetDomainStatsDays | Unset):  Default: GetDomainStatsDays.VALUE_7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DomainStats | Error]
    """

    kwargs = _get_kwargs(
        host=host,
        days=days,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    host: str,
    days: GetDomainStatsDays | Unset = GetDomainStatsDays.VALUE_7,
) -> DomainStats | Error | None:
    """How the whole platform does on one host

     Free. The numbers are the whole platform's, per host: shop.example.com
    and example.com are two answers, and www. is dropped. They are rolled
    up every hour, at 20 minutes past, so a fetch shows within about 80
    minutes, today included. Only fetches that reached the site count:
    refusals before the fetch (balance, limits, capacity) are left out. A
    breakdown line is shown only when at least 3 customers and at least
    20 requests are behind it in the window, and requests counts only
    the lines shown; with no line left the answer is requests 0 and an
    empty breakdown. Customers are counted per day, so a line whose
    customers came on different days can stay hidden. The answer is
    cached for five minutes.

    Error codes bad_parameter, bad_token, internal, wrong_scope.

    Args:
        host (str):
        days (GetDomainStatsDays | Unset):  Default: GetDomainStatsDays.VALUE_7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DomainStats | Error
    """

    return sync_detailed(
        client=client,
        host=host,
        days=days,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    host: str,
    days: GetDomainStatsDays | Unset = GetDomainStatsDays.VALUE_7,
) -> Response[DomainStats | Error]:
    """How the whole platform does on one host

     Free. The numbers are the whole platform's, per host: shop.example.com
    and example.com are two answers, and www. is dropped. They are rolled
    up every hour, at 20 minutes past, so a fetch shows within about 80
    minutes, today included. Only fetches that reached the site count:
    refusals before the fetch (balance, limits, capacity) are left out. A
    breakdown line is shown only when at least 3 customers and at least
    20 requests are behind it in the window, and requests counts only
    the lines shown; with no line left the answer is requests 0 and an
    empty breakdown. Customers are counted per day, so a line whose
    customers came on different days can stay hidden. The answer is
    cached for five minutes.

    Error codes bad_parameter, bad_token, internal, wrong_scope.

    Args:
        host (str):
        days (GetDomainStatsDays | Unset):  Default: GetDomainStatsDays.VALUE_7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DomainStats | Error]
    """

    kwargs = _get_kwargs(
        host=host,
        days=days,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    host: str,
    days: GetDomainStatsDays | Unset = GetDomainStatsDays.VALUE_7,
) -> DomainStats | Error | None:
    """How the whole platform does on one host

     Free. The numbers are the whole platform's, per host: shop.example.com
    and example.com are two answers, and www. is dropped. They are rolled
    up every hour, at 20 minutes past, so a fetch shows within about 80
    minutes, today included. Only fetches that reached the site count:
    refusals before the fetch (balance, limits, capacity) are left out. A
    breakdown line is shown only when at least 3 customers and at least
    20 requests are behind it in the window, and requests counts only
    the lines shown; with no line left the answer is requests 0 and an
    empty breakdown. Customers are counted per day, so a line whose
    customers came on different days can stay hidden. The answer is
    cached for five minutes.

    Error codes bad_parameter, bad_token, internal, wrong_scope.

    Args:
        host (str):
        days (GetDomainStatsDays | Unset):  Default: GetDomainStatsDays.VALUE_7.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DomainStats | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            host=host,
            days=days,
        )
    ).parsed
