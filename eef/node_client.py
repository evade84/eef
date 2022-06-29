from typing import Any, Dict, NoReturn, Optional

import requests

from eef.config import config
from eef.models import Message, Messages, Node, Pool, Pools
from eef.output import error


class NodeClient:
    def __init__(self):
        self.node_url = config.read_node_url()

    @staticmethod
    def _get_error_message(resp: requests.Response) -> str | None:
        return resp.json().get("error_message")

    def api_request(
        self,
        method: str,
        route: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> NoReturn | Dict[str, Any]:
        try:
            resp = requests.request(
                method, f"{self.node_url}{route}", params=params, json=body
            )
            match resp.status_code:
                case 200:  # success
                    return resp.json()
                case 400:  # input data is incorrect
                    error(
                        f"API request input data is incorrect: {self._get_error_message(resp).lower()}",
                        terminate=True,
                    )
                case 403:  # access denied
                    error(self._get_error_message(resp).lower(), terminate=True)
                case 404:  # not found
                    error(self._get_error_message(resp).lower(), terminate=True)
                case 409:  # conflict
                    error(self._get_error_message(resp).lower(), terminate=True)
                case 422:  # validation error
                    error(
                        f"API request validation error: {resp.json()}.", terminate=True
                    )
                case _:
                    error(
                        f"invalid response code from the node: {resp.status_code}.",
                        terminate=True,
                    )
        except requests.exceptions.ConnectionError:
            error(f"could not connect to the node ({self.node_url}).", terminate=True)

    def pool_info(
        self,
        identifier: str,
        master_key: Optional[str] = None,
        reader_key: Optional[str] = None,
    ) -> Pool:
        resp = self.api_request(
            "get",
            f"/pool/{identifier}",
            params={"master_key": master_key, "reader_key": reader_key},
        )
        return Pool(**resp)

    def pool_list(self, first: Optional[int] = None, last: Optional[int] = None) -> Pools:
        resp = self.api_request(
            "get", "/pool/list", params={"first": first, "last": last}
        )
        return Pools(**resp)

    def pool_new(
        self,
        tag: Optional[str] = None,
        master_key: Optional[str] = None,
        reader_key: Optional[str] = None,
        creator: Optional[str] = None,
        description: Optional[str] = None,
        indexable: Optional[bool] = None,
    ) -> Pool:
        resp = self.api_request(
            "post",
            "/pool/new",
            body={
                "tag": tag,
                "master_key": master_key,
                "reader_key": reader_key,
                "creator": creator,
                "description": description,
                "indexable": indexable,
            },
        )
        return Pool(**resp)

    def pool_read(
        self,
        identifier: str,
        first: Optional[int] = None,
        last: Optional[int] = None,
        master_key: Optional[str] = None,
        reader_key: Optional[str] = None,
    ) -> Messages:
        resp = self.api_request(
            "get",
            f"/pool/{identifier}/read",
            params={
                "first": first,
                "last": last,
                "master_key": master_key,
                "reader_key": reader_key,
            },
        )
        return Messages(**resp)

    def pool_write(
        self,
        identifier: str,
        text: str,
        signature: Optional[str] = None,
        master_key: Optional[str] = None,
    ) -> Message:
        resp = self.api_request(
            "put",
            f"/pool/{identifier}/write",
            {
                "text": text,
                "signature": signature,
                "master_key": master_key,
            },
        )
        return Message(**resp)

    def node(self):
        resp = self.api_request("get", "/node")
        return Node(**resp)
