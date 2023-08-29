import json
from datetime import datetime
from typing import Any, Dict, List

import requests
from azure.identity import ClientSecretCredential

from .exceptions import (
    DataverseAuthenticationError,
    DataverseConnectionError,
    DataverseHttpError,
    DataverseUserPermissionError,
)


class DataverseClient:
    http_error_classes = {
        401: DataverseUserPermissionError,
        403: DataverseUserPermissionError,
        "default": DataverseHttpError,
    }

    def __init__(
        self,
        api_hostname: str,
        api_version: float,
        client_id: str,
        tenant_id: str,
        client_secret: str,
    ):
        self.api_hostname = api_hostname
        self.api_version = api_version
        self.base_url = "https://{0}/api/data/v{1}".format(api_hostname, api_version)
        self.timeout = 10
        self._access_token = None
        self._access_token_expires = None
        self._access_token_generator = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

    @classmethod
    def handle_http_error(cls, response: requests.Response) -> None:
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # Raise a more specific (custom) error
            new_class = (
                cls.http_error_classes.get(response.status_code, None)
                or cls.http_error_classes["default"]
            )
            try:
                response_body = json.dumps(response.json(), indent=4)
            except ValueError:
                response_body = response.content
            new_error = new_class("{}. Response body:\n{}".format(e, response_body))
            new_error.response = response
            raise new_error from e

    def get(self, path: str, params=None) -> requests.Response:
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        token = self.get_access_token()
        try:
            response = requests.get(
                url, params=params, headers={"Authorization": f"Bearer {token}"}
            )
        except requests.ConnectionError:
            raise DataverseConnectionError
        self.handle_http_error(response)
        return response

    def get_access_token(self) -> str:
        if (
            self._access_token is None
            or self._access_token_expires is None
            or self._access_token_expires >= datetime.now()
        ):
            try:
                result = self._access_token_generator.get_token(
                    f"https://{self.api_hostname}/.default"
                )
            except Exception:
                raise DataverseAuthenticationError
            else:
                self._access_token = result.token
                self._access_token_expires = datetime.fromtimestamp(result.expires_on)
        return self._access_token

    def get_rows(
        self,
        table_id: str,
        columns: List[str] = None,
        order_by: str = None,
        extra_params: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        params = {}
        if columns:
            params["$select"] = ",".join(columns)
        if order_by:
            params["$orderby"] = order_by
        if extra_params:
            params.update(extra_params)
        return self.get(table_id, params).json()["value"]

    def get_row(self, table_id: str, id: str) -> Dict[str, Any]:
        return self.get(table_id + f"({id})").json()
