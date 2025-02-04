from urllib.parse import urlparse, urlunparse,urljoin
import requests
import re


def get_hostname(url):
    parsed_url = urlparse(url)
    # Rebuild the URL with only scheme and netloc (without path, params, query, and fragment)
    normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    return normalized_url


def get_site_name(url):
    return urlparse(url).hostname


def normalize_url(base_url, href):

    full_url = urljoin(base_url, href)
    parsed_url = urlparse(full_url)
    normalized_url = parsed_url.geturl()

    if normalized_url.endswith('/'):
        normalized_url = normalized_url[:-1]

    return normalized_url


def is_file_url(url):
    file_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg','.pdf')

    return url.lower().endswith(file_extensions)


def get_robots_txt_disallowed_urls(base_url):

    robots_url = urljoin(base_url, "/robots.txt")

    try:
        response = requests.get(robots_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        disallowed_urls = []

        for line in response.text.splitlines():
            if line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    full_url = urljoin(base_url, path)
                    disallowed_urls.append(full_url)

        return disallowed_urls

    except requests.exceptions.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return []



def detect_hotel_string(input_string):
    # Define the regex pattern
    pattern = r'^/hotels/\d+'

    # Use re.match to check if the input string matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False