import pytz
import json

user_timezone = input("Enter your timezone: ").strip()

try:
    pytz.timezone(user_timezone)
except pytz.UnknownTimeZoneError:
    print("That was not a valid timezone.")
    raise

with open("user_config.json", "w") as config:
    json.dump({"timezone": user_timezone}, config)