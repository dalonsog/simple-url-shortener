import re

def validate_email(email: str) -> bool:
    if not email:
        return False
    
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(regex, email)
    return True if match else False


def validate_url(url: str) -> bool:
    if not url:
        return False
    
    regex = ("((http|https)://)(www.)?" + 
             "[a-zA-Z0-9@:%._\\+~#?&//=]" + 
             "{2,256}\\.[a-z]" + 
             "{2,6}\\b([-a-zA-Z0-9@:%" + 
             "._\\+~#?&//=]*)")
    
    pattern = re.compile(regex)
    if re.search(pattern, str):
        return True
    else:
        return False
