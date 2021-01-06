"""
Logger is an independent module that logs data to a file. Logger should not rely on other modules
for anything other than initialisation and sending of data to log. Logger is designed to operate
assuming every other module (excluding orb_core) is broken.
"""
from datetime import datetime

def log(source, content):
    """
    Logs a message to the file
    """
    # Builds or opens log file
    with open("log.txt", mode="a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()}: [{source}] {content}\n")

def log_and_print(source, content):
    print(f"[{source}] {content}")
    log(source, content)