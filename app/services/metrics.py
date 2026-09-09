from __future__ import annotations

from threading import Lock


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self._http_requests: dict[tuple[str, int], int] = {}
        self._http_duration_ms = 0.0
        self._workflow_outcomes: dict[str, int] = {"success": 0, "failure": 0}

    def record_http_request(self, method: str, status_code: int, duration_ms: float) -> None:
        with self._lock:
            key = (method, status_code)
            self._http_requests[key] = self._http_requests.get(key, 0) + 1
            self._http_duration_ms += duration_ms

    def record_workflow(self, outcome: str) -> None:
        with self._lock:
            self._workflow_outcomes[outcome] = self._workflow_outcomes.get(outcome, 0) + 1

    def render_prometheus(self) -> str:
        with self._lock:
            lines = [
                "# HELP ai_operations_http_requests_total Total HTTP requests.",
                "# TYPE ai_operations_http_requests_total counter",
            ]
            for (method, status_code), count in sorted(self._http_requests.items()):
                lines.append(
                    f'ai_operations_http_requests_total{{method="{method}",status="{status_code}"}} {count}'
                )
            lines.extend(
                [
                    "# HELP ai_operations_http_request_duration_ms_sum Total HTTP request duration in milliseconds.",
                    "# TYPE ai_operations_http_request_duration_ms_sum counter",
                    f"ai_operations_http_request_duration_ms_sum {self._http_duration_ms:.3f}",
                    "# HELP ai_operations_workflow_executions_total Workflow outcomes.",
                    "# TYPE ai_operations_workflow_executions_total counter",
                ]
            )
            for outcome, count in sorted(self._workflow_outcomes.items()):
                lines.append(f'ai_operations_workflow_executions_total{{outcome="{outcome}"}} {count}')
            return "\n".join(lines) + "\n"


metrics = MetricsRegistry()