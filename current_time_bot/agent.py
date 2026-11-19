from google.adk.agents.llm_agent import Agent
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from google.adk.models.lite_llm import LiteLlm


def get_current_time(timezone: str) -> dict:
    """Get the current date and time in a given time zone.

    Use this whenever the user asks what time or date it is somewhere.

    Args:
        timezone: A string representing the IANA time zone (e.g. "Asia/Kolkata").

    Returns:
        A dict with "status" ("success" or "error"). On success it also has
        "timezone", "date", "time" and "weekday". On error it has "error_message".
    """
    try:
        now = datetime.now(ZoneInfo(timezone))
    except ZoneInfoNotFoundError:
        return {
            "status": "error",
            "error_message": f"Unknown time zone '{timezone}'. Use an IANA name like 'Asia/Kolkata'.",
        }
    return {
        "status": "success",
        "timezone": timezone,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "weekday": now.strftime("%A"),
    }

root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-120b"),
    name='root_agent',
    description='Tells the current time and date anywhere in the world.',
    instruction="""
You are a real-time World Clock Assistant.

Your responsibility is to provide the current date and time
for any city or country.

STRICT RULES:

1. Always call get_current_time before answering
   any question about current date or time.

2. Convert the city into its correct IANA timezone.

3. Examples:
   London -> Europe/London
   Mumbai -> Asia/Kolkata
   New York -> America/New_York
   Tokyo -> Asia/Tokyo
   Dubai -> Asia/Dubai

4. If the tool returns success:
   Display city, date, time, weekday and timezone.

5. If the tool returns an error:
   Do not invent the time.
   Do not provide lengthy apologies.
   Do not suggest external websites.
   Briefly explain that the time service is unavailable.

6. Never claim that all timezones are failing
   based on a single failed request.

7. Never calculate or guess the current time yourself.

Keep responses short and conversational.
""",
    tools=[get_current_time],
)
