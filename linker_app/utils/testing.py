from bs4 import BeautifulSoup


def get_csrf_token(client, url):
    """ find first csrf token on page """
    response = client.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'}).get('value')
    return csrf_token


def get_correct_links():
    success_data = (
        'http://127.0.0.1:5000/links',
        'https://www.some-url.com/path',
        'https://chat.openai.com/',
        'https://flask-wtf.readthedocs.io/en/',

        "http://www.google.com",
        "https://www.google.com",
        "http://google.com",
        "https://google.com",
        "http://www.google.com/~as_db3.2123/134-1a",
        "https://www.google.com/~as_db3.2123/134-1a",
        "http://google.com/~as_db3.2123/134-1a",
        "https://google.com/~as_db3.2123/134-1a",
        # .co.uk top level
        "http://www.google.co.uk",
        "https://www.google.co.uk",
        "http://google.co.uk",
        "https://google.co.uk",
        "http://www.google.co.uk/~as_db3.2123/134-1a",
        "https://www.google.co.uk/~as_db3.2123/134-1a",
        "http://google.co.uk/~as_db3.2123/134-1a",
        "https://google.co.uk/~as_db3.2123/134-1a",
    )
    return success_data


def get_failed_links():
    failed_data = (
        'not-url',
        '1231.com',
        # data without protocol
        "google.com",
        "google.co.uk",
        "google.co.uk/~as_db3.2123/134-1a",
        "www.google.com",
        "www.google.co.uk",
        "www.google.com/~as_db3.2123/134-1a",
        "google.com/~as_db3.2123/134-1a",
    )
    return failed_data
