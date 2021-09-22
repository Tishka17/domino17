from datetime import datetime
from typing import Any, List

from dataclass_factory import Factory, NameStyle, Schema

from .base import DominoBase
from .models.environments import EnvironmentList
from .models.files import UploadResult
from .models.run import NewRun, Run, RunList, RunLogs
from .models.search import SearchArea


def parse_timestamp(data):
    return datetime.utcfromtimestamp(data / 1000)


class Domino(DominoBase):

    def _create_factory(self) -> Factory:
        return Factory(
            debug_path=True,
            default_schema=Schema(name_style=NameStyle.camel_lower),
            schemas={
                datetime: Schema(parser=parse_timestamp),
            },
        )

    # runs
    def start_run(
            self, user: str, project: str, command: List[str], *,
            title: str = "", commit_id: str = "", is_direct: bool = False, tier: str = "",
            dataset_config: str = "",
    ) -> NewRun:
        data = {
            "isDirect": is_direct,
            "command": command,
        }
        if title:
            data["title"] = title
        if dataset_config:
            data["datasetConfig"] = dataset_config
        if tier:
            data["tier"] = tier
        if commit_id:
            data["commitId"] = commit_id
        return self._post(f"v1/projects/{user}/{project}/runs", json=data, model=NewRun)

    def run_status(self, user: str, project: str, run_id: str) -> Run:
        return self._get(f"v1/projects/{user}/{project}/runs/{run_id}/", model=Run)

    def runs(self, user: str, project: str) -> RunList:
        return self._get(f"v1/projects/{user}/{project}/runs", model=RunList)

    def run_logs(self, user: str, project: str, run_id: str, limit: int = 20) -> RunLogs:
        return self._get(f"v1/projects/{user}/{project}/run/{run_id}/stdout",
                         params={"previewNumberOfLines": limit},
                         model=RunLogs)

    # files
    def files(self, user: str, project: str, commit: str, path: str = ""):
        return self._request(f"v1/projects/{user}/{project}/files/{commit}/{path}", method="GET").json()

    def file(self, url, raw: bool = True):
        response = self._request(url, method="GET", stream=True)
        if raw:
            return response.raw
        else:
            return response.content

    def upload(self, user: str, project: str, path: str, data: bytes) -> UploadResult:
        return self._put(f"v1/projects/{user}/{project}/{path}", data=data, model=UploadResult)

    # search
    def search(self, query: str, area: SearchArea) -> Any:
        return self._get("v1/search", params={"query": query, "area": area.value})

    # environments
    def environments(self) -> EnvironmentList:
        return self._get("v1/environments", model=EnvironmentList)
