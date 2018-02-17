import re

def extract_with_css(element, selector):
    text = element.css(selector).extract_first()
    return text.strip() if text else None

def only_digit(text):
    return re.sub(r'\D', '', text)
