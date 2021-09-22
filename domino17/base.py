from typing import Any, Dict, Optional, overload, Type, TypeVar

from dataclass_factory import Factory
from requests import RequestException, Session

from .exceptions import DominoException

TRIAL_URL = "https://try.dominodatalab.com"
PRODUCTION_URL = "https://api.dominodatalab.com"

T = TypeVar("T")


class DominoBase:
    def __init__(self, token: str, *,
                 session: Optional[Session] = None,
                 base_url: Optional[str] = None,
                 trial: bool = False):
        self.token = token
        self.session = session or Session()
        if base_url is None:
            base_url = TRIAL_URL if trial else PRODUCTION_URL
        self.base_url = base_url.rstrip("/") + "/"  # keep only one / at the end
        self.factory = self._create_factory()

    def _create_factory(self) -> Factory:
        return Factory(debug_path=True)

    def _request(
            self,
            path: str,
            *,
            method: str,
            params: Optional[Dict[str, Any]] = None,
            json=None,
            data=None,
            stream=False,
    ):
        if not path.startswith("https://"):
            path = self.base_url + path
        try:
            headers = {
                "X-Domino-Api-Key": self.token,
            }
            resp = self.session.request(
                method,
                path,
                params=params, json=json, data=data,
                headers=headers, stream=stream,
            )
            resp.raise_for_status()
            return resp
        except RequestException as e:
            raise DominoException from e

    @overload
    def _get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        ...

    @overload
    def _get(self, path: str, *, model: Type[T], params: Optional[Dict[str, Any]] = None) -> T:
        ...

    def _get(self, path: str, *, model=Any, params: Optional[Dict[str, Any]] = None):
        return self.factory.load(
            self._request(path, method="GET", params=params).json(),
            model,
        )

    @overload
    def _post(self, path, *,
              params: Optional[Dict[str, Any]] = None, json=None, data=None) -> Any:
        ...

    @overload
    def _post(self, path, *,
              model: Type[T], params: Optional[Dict[str, Any]] = None, json=None, data=None) -> T:
        ...

    def _post(self, path, *,
              model=Any, params: Optional[Dict[str, Any]] = None, json=None, data=None):
        return self.factory.load(
            self._request(path, method="POST", json=json, data=data, params=params).json(),
            model,
        )

    @overload
    def _put(self, path, *,
             params: Optional[Dict[str, Any]] = None, json=None, data=None) -> Any:
        ...

    @overload
    def _put(self, path, *,
             model: Type[T], params: Optional[Dict[str, Any]] = None, json=None, data=None) -> T:
        ...

    def _put(self, path, *,
             model=Any, params: Optional[Dict[str, Any]] = None, json=None, data=None):
        return self.factory.load(
            self._request(path, method="PUT", json=json, data=data, params=params).json(),
            model,
        )
