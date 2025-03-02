import pycountry
from datetime import datetime
import base64
import re
import string

def is_valid_gender(gender_input):
    valid_genders = ["nam", "nữ", "m", "f", "male", "female"]
    
    if gender_input.strip().lower() in valid_genders:
        return True
    return False

def is_valid_nationality(nationality_input):
    nationality_input = nationality_input.strip().lower()
    if nationality_input == "VN":
        return True
    for country in pycountry.countries:
        if nationality_input == country.name.lower():
            return True
        if nationality_input == country.alpha_3.lower():
            return True

    return False

def is_valid_marital_status(status_input):
    valid_statuses = ["chưa kết hôn", "độc thân", "đã kết hôn", "kết hôn", "ly hôn", "góa"]

    if status_input.strip().lower() in valid_statuses:
        return True
    return False

def is_valid_birthday(birthday_input):
    date_formats = ["%d.%m.%Y", "%Y", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d"]
    
    for date_format in date_formats:
        try:
            datetime.strptime(birthday_input, date_format)
            return True
        except ValueError:
            continue
    return False

def is_base64(s):
    try:
        if len(s) % 4 == 0:
            decoded = base64.b64decode(s, validate=True)
            return True
    except Exception:
        return False
    return False

def is_random_text(s):
    valid_characters = string.ascii_letters + string.digits + string.punctuation
    for char in s:
        if char not in valid_characters:
            return False
    char_frequencies = {}
    for char in s:
        if char not in char_frequencies:
            char_frequencies[char] = 1
        else:
            char_frequencies[char] += 1
    if len(char_frequencies) / len(s) > 0.7:
        return True
    return False

def is_encrypted(text):
    text = text.strip()
    if len(text) < 10:
        return False
    if is_base64(text):
        return True
    if is_random_text(text):
        return True

    return False

def is_valid_email(text):
    email_regex = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    if re.match(email_regex, text):
        return True
    return False

def check_rules(text):
    if is_valid_nationality(text):
        return "LABEL_3"
    elif is_valid_marital_status(text):
        return "LABEL_3"
    elif is_valid_gender(text):
        return "LABEL_3"
    elif is_valid_birthday(text):
        return "LABEL_3"
    elif is_encrypted(text):
        return "LABEL_3"
    elif is_valid_email(text):
        return "LABEL_3"
    else:
        return -1