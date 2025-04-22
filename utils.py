from datetime import datetime
import pytz

def combine_date_time(date_str, time_str, timezone="Asia/Seoul") -> str:
    combined = f"{date_str} {time_str}"
    dt = datetime.strptime(combined, "%b %d, %Y %H:%M")
    local_tz = pytz.timezone(timezone)
    localized_dt = local_tz.localize(dt)
    return localized_dt.isoformat()