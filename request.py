from app.models import Quotes
from config import Config
import urllib.request,json
quotes_url = Config.QUOTES_URL


def get_quotes():
    ''''
    Function  that processes the Quotes result and transform them to a list of Objects
    '''
    get_quotes_url = quotes_url.format()
    with urllib.request.urlopen(get_quotes_url) as url:
        articles_results = json.loads(url.read())
        article_object = None
        if articles_results:
            author=articles_results.get('author')
            quote = articles_results.get('quote')
            permalink = articles_results.get('permalink')
            article_object = Quotes(author,quote,permalink)
    return article_object
