from datetime import datetime, timezone


def now_as_iso8601():
    now = datetime.now(tz=timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
