import re

def is_exit(text):
    return bool(re.search(r"\b(bye|quit|exit)\b", text.lower()))

def is_greeting(text):
    return bool(re.search(r"\b(hi|hello|hey)\b", text.lower()))
