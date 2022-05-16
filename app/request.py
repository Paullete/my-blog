import requests
from .models import Quote

URL = 'http://quotes.stormconsultancy.co.uk/random.json'


def get_quote():
    """
    method that fetches data from api and create a Quote instance
    :return: Quote instance
    """
    response = requests.get(URL).json()
    random_quote = Quote(response.get('author'), response.get('quote'))
    return random_quote