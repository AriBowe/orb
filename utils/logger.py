import json

utilDef = json.loads("""{
    "type": "logger",
    "name": "logger",
    "selftest": 1,
    "requires": [
    ]
}""")

# Priorities are as follows:
# 1: Notice         (Business as usual)
# 2: Alert          (Something unusual happened, but nothing broke)
# 3: Error          (Something failed)
# 4: Major Error    (A large section of the bot is broken, e.g. database failure)
# 5: Critical Error (The bot is unable to function at all)

from datetime import datetime

logf = open("log.txt", "at")

# Logs an event
def _log(content, source="unknown", priority="1"):
    log = f"{datetime.now().replace(microsecond=0)}: [{source}]\t{content}"
    print(log)
    if priority > 1:
        logf.write(log)

# Register a module or util with the logger
def register(name):
    return lambda c, p=1 : _log(c, source=name, priority=p)