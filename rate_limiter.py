from datetime import datetime, timezone


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def is_allowed(self, client_id: str) -> bool:
        now = datetime.now(timezone.utc)

        if client_id not in self.requests:
            self.requests[client_id] = []

        recent_requests = []

        for request_time in self.requests[client_id]:
            age = (now - request_time).total_seconds()

            if age < self.window_seconds:
                recent_requests.append(request_time)

        self.requests[client_id] = recent_requests

        if len(self.requests[client_id]) >= self.max_requests:
            return False

        self.requests[client_id].append(now)
        return True

    def reset(self):
        self.requests = {}