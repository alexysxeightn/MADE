"""Flask webapp for query wikipedia"""
import logging.config
from bs4 import BeautifulSoup
from flask import Flask, request, abort, jsonify
from flask.logging import create_logger
import yaml
import requests


WIKI_BASE_URL = "https://en.wikipedia.org"
WIKI_BASE_SEARCH_URL = f"{WIKI_BASE_URL}/w/index.php?search="


logging.config.dictConfig(yaml.safe_load("""
version: 1
formatters:
    simple:
        format: "%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s"
        datefmt: "%Y%m%d_%H%M%S"
handlers:
    stream_handler:
        class: logging.StreamHandler
        stream: ext://sys.stderr
        level: DEBUG
        formatter: simple
    file_handler:
        class: logging.FileHandler
        filename: wiki_search_app.log
        level: DEBUG
        formatter: simple
loggers:
    task_Khmelev_Alexey_web_service_log:
        level: DEBUG
        propogate: False
        handlers:
            - stream_handler
            - file_handler
    werkzeug:
        level: DEBUG
        propogate: False
        handlers:
            - stream_handler
"""))


app = Flask(__name__)
app.logger = create_logger(app)


def parse_wiki_search(html_data: str) -> int:
    """Function for parsing wiki (num documents for query)"""
    wiki_soup = BeautifulSoup(html_data, features='html.parser')

    article_count = wiki_soup.find(
        "div",
        attrs={"class": "results-info"}
    )

    if article_count:
        article_count = article_count.find_all("strong")[1].text
        article_count = int(article_count.replace(',', ''))
        return article_count

    return 0


@app.route("/api/search")
def search_on_wiki():
    """Return result of user queries"""
    query = request.args.get("query", "")
    app.logger.debug("start processing query: %s", query)
    try:
        wiki_responce = requests.get(WIKI_BASE_SEARCH_URL + query)
        article_count = parse_wiki_search(wiki_responce.text)
        app.logger.info("found %s articles for query: %s", article_count, query)
        app.logger.debug("finish processing query: %s", query)
        return jsonify({
            "version": 1.0,
            "article_count": article_count,
        })
    except requests.ConnectionError:
        abort(503)


@app.errorhandler(404)
def page_do_not_exist(error):
    """Exception for 404 error"""
    return "This route is not found", 404


@app.errorhandler(503)
def page_return_503(error):
    """Exception for 503 error"""
    return "Wikipedia Search Engine is unavailable", 503


if __name__ == '__main__':
    app.run()
