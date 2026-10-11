from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.scrape_envelope import ScrapeEnvelope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ScrapeEnvelope,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

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
    body: ScrapeEnvelope,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | str]:
    """Scrape a URL from a JSON envelope and stream the result

     The canonical call. One JSON object, at most 1 MB, whose keys are the
    parameter names of the GET plus method, body and content_type. Nothing
    of ours travels in the query string here, so a target URL is sent as
    it is with no encoding. The token is the Authorization header, and
    the body is not read until the token is verified.
    Every value is a string; headers is a list of strings. An unknown key
    is a 400, exactly as on the GET, and so is any query string on this
    route: a parameter left there would not be read.
    QUERY /v1 is accepted with this exact request body, on the same code
    path: same parameters, same errors, same Idempotency-Key, same price,
    only the method word changes. It is the RFC 10008 standards path
    (Proposed Standard, June 2026) for a request that carries a body and
    is safe and idempotent. It is described here rather than as its own
    operation because the query path item field arrived in OpenAPI 3.2 and
    this document is 3.1. POST stays the example either way: browsers are
    still evaluating QUERY and an older WAF or proxy may refuse a method
    it does not know.

    Args:
        idempotency_key (str | Unset):
        body (ScrapeEnvelope): The POST /v1 request body. Every value is a string, except headers,
            which is a list of strings. An unknown key is a 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
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
    body: ScrapeEnvelope,
    idempotency_key: str | Unset = UNSET,
) -> Error | str | None:
    """Scrape a URL from a JSON envelope and stream the result

     The canonical call. One JSON object, at most 1 MB, whose keys are the
    parameter names of the GET plus method, body and content_type. Nothing
    of ours travels in the query string here, so a target URL is sent as
    it is with no encoding. The token is the Authorization header, and
    the body is not read until the token is verified.
    Every value is a string; headers is a list of strings. An unknown key
    is a 400, exactly as on the GET, and so is any query string on this
    route: a parameter left there would not be read.
    QUERY /v1 is accepted with this exact request body, on the same code
    path: same parameters, same errors, same Idempotency-Key, same price,
    only the method word changes. It is the RFC 10008 standards path
    (Proposed Standard, June 2026) for a request that carries a body and
    is safe and idempotent. It is described here rather than as its own
    operation because the query path item field arrived in OpenAPI 3.2 and
    this document is 3.1. POST stays the example either way: browsers are
    still evaluating QUERY and an older WAF or proxy may refuse a method
    it does not know.

    Args:
        idempotency_key (str | Unset):
        body (ScrapeEnvelope): The POST /v1 request body. Every value is a string, except headers,
            which is a list of strings. An unknown key is a 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ScrapeEnvelope,
    idempotency_key: str | Unset = UNSET,
) -> Response[Error | str]:
    """Scrape a URL from a JSON envelope and stream the result

     The canonical call. One JSON object, at most 1 MB, whose keys are the
    parameter names of the GET plus method, body and content_type. Nothing
    of ours travels in the query string here, so a target URL is sent as
    it is with no encoding. The token is the Authorization header, and
    the body is not read until the token is verified.
    Every value is a string; headers is a list of strings. An unknown key
    is a 400, exactly as on the GET, and so is any query string on this
    route: a parameter left there would not be read.
    QUERY /v1 is accepted with this exact request body, on the same code
    path: same parameters, same errors, same Idempotency-Key, same price,
    only the method word changes. It is the RFC 10008 standards path
    (Proposed Standard, June 2026) for a request that carries a body and
    is safe and idempotent. It is described here rather than as its own
    operation because the query path item field arrived in OpenAPI 3.2 and
    this document is 3.1. POST stays the example either way: browsers are
    still evaluating QUERY and an older WAF or proxy may refuse a method
    it does not know.

    Args:
        idempotency_key (str | Unset):
        body (ScrapeEnvelope): The POST /v1 request body. Every value is a string, except headers,
            which is a list of strings. An unknown key is a 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
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
    body: ScrapeEnvelope,
    idempotency_key: str | Unset = UNSET,
) -> Error | str | None:
    """Scrape a URL from a JSON envelope and stream the result

     The canonical call. One JSON object, at most 1 MB, whose keys are the
    parameter names of the GET plus method, body and content_type. Nothing
    of ours travels in the query string here, so a target URL is sent as
    it is with no encoding. The token is the Authorization header, and
    the body is not read until the token is verified.
    Every value is a string; headers is a list of strings. An unknown key
    is a 400, exactly as on the GET, and so is any query string on this
    route: a parameter left there would not be read.
    QUERY /v1 is accepted with this exact request body, on the same code
    path: same parameters, same errors, same Idempotency-Key, same price,
    only the method word changes. It is the RFC 10008 standards path
    (Proposed Standard, June 2026) for a request that carries a body and
    is safe and idempotent. It is described here rather than as its own
    operation because the query path item field arrived in OpenAPI 3.2 and
    this document is 3.1. POST stays the example either way: browsers are
    still evaluating QUERY and an older WAF or proxy may refuse a method
    it does not know.

    Args:
        idempotency_key (str | Unset):
        body (ScrapeEnvelope): The POST /v1 request body. Every value is a string, except headers,
            which is a list of strings. An unknown key is a 400.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
