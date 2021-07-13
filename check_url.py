import re


def check_url(url):
    url_pattern = '^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+$'
    if re.match(url_pattern, url):
        return url
    else:
        return 'URL is not valid.'
