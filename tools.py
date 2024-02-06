from datetime import datetime, time, timedelta


def seconds_until_target_time(t: str):
    target_hour, target_minute, target_second = map(int, t.split(":"))

    now = datetime.now()

    target_time = time(target_hour, target_minute, target_second)

    if now.time() >= target_time:
        tomorrow = now + timedelta(days=1)
        target_datetime = datetime.combine(tomorrow.date(), target_time)

    else:
        target_datetime = datetime.combine(now.date(), target_time)

    time_difference = target_datetime - now

    seconds_until_target = time_difference.total_seconds()

    return seconds_until_target
