from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional


class RunStatus(Enum):
    PENDING = "Pending"
    QUEUED = "Queued"
    SCHEDULED = "Scheduled"
    PREPARING = "Preparing"
    BUILDING = "Building"
    PULLING = "Pulling"
    RUNNING = "Running"
    SERVING = "Serving"
    STOP_REQUESTED = "StopRequested"
    STOP_AND_DISCARD_REQUESTED = "StopAndDiscardRequested"
    STOPPING = "Stopping"
    FINISHING = "Finishing"
    STOPPED = "Stopped"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    ERROR = "Error"


@dataclass
class NewRun:
    run_id: str
    message: str


@dataclass
class RunLogs:
    setup: str
    stdout: str


@dataclass
class Data:
    key: str
    value: Any


@dataclass
class DiagnosticStatistics:
    is_error: bool
    data: List[Data]


@dataclass
class Run:
    id: str
    project_id: str
    number: int
    starting_user_id: str
    queued: Optional[datetime]
    started: Optional[datetime]
    completed: Optional[datetime]
    status: RunStatus
    commit_id: str
    executor: Optional[str]
    output_commit_id: Optional[str]
    title: Optional[str]
    is_archived: bool
    post_processed_timestamp: Optional[datetime]
    diagnostic_statistics: Optional[DiagnosticStatistics]
    is_completed: bool
    hardware_tier_id: str


@dataclass
class RunList:
    object_type: str
    url: str
    data: List[Run]
