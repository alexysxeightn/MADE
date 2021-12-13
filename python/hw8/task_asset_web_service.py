"""Flask webapp for work with assets"""
from typing import Dict
from bs4 import BeautifulSoup
from flask import Flask, request, abort, jsonify
import requests


URL_CBR_CURRENCY_BASE_DAILY = 'https://www.cbr.ru/eng/currency_base/daily'
URL_CBR_KEY_INDICATORS = 'https://www.cbr.ru/eng/key-indicators/'
CHAR_CODES_FOR_KEY_INDICATORS = ["USD", "EUR", "Au", "Ag", "Pd", "Pt"]


class Asset:
    """Class for save asset information and calculate revenue"""
    def __init__(self, char_code: str, name: str, capital: float, interest: float):
        self.char_code = char_code
        self.name = name
        self.capital = capital
        self.interest = interest

    def calculate_revenue(self, year: int) -> float:
        """Calculate revenue of asset for get year"""
        revenue = self.capital * ((1.0 + self.interest) ** year - 1.0)
        return revenue

    def get_params(self) -> list:
        """Return list of params to asset"""
        return [self.char_code, self.name, self.capital, self.interest]


app = Flask(__name__)
app.bank = dict()


def parse_cbr_currency_base_daily(html_data: str) -> Dict[str, float]:
    """Function for parsing https://www.cbr.ru/eng/currency_base/daily"""
    cbr_soup = BeautifulSoup(html_data, features='html.parser')
    rates = dict()

    table = cbr_soup.find_all("table", attrs={"class": "data"})[0].find("tbody")
    for row in table.find_all('tr'):
    	if row.find('td'):
            columns = [x.text for x in row.find_all('td')]
            rates[columns[1]] = float(columns[4]) / float(columns[2])

    return rates


def parse_cbr_key_indicators(html_data: str) -> Dict[str, float]:
    """Function for parsing https://www.cbr.ru/eng/key-indicators/"""
    cbr_soup = BeautifulSoup(html_data, features='html.parser')
    rates = dict()

    dropdown_collection = cbr_soup.find_all("div", attrs={"class": "dropdown"})
    for dropdown_ in dropdown_collection:
        dropdown = dropdown_.find("div", attrs={"class": "dropdown_title _active"})
        if dropdown:
            dropdown = dropdown_
            break

    table_collection = dropdown.find_all(
        "div",
        attrs={"class": "key-indicator_content offset-md-2"}
    )

    for table in table_collection:
        if table.find("div", attrs={"class": "d-flex flex-column flex-md-row title-date"}):
            continue
        if table.find("tr"):
            for row in table.find_all("tr")[1:]:
                char_code = row.find_all("td")[0].find_all("div")[2].text
                rate = row.find_all("td")[-1]
                rate = float(rate.text.replace(',', ''))
                rates[char_code] = rate

    return rates


@app.route("/cbr/daily")
def cbr_currency_base_daily():
    """Function for return result of parsing
    https://www.cbr.ru/eng/currency_base/daily"""
    try:
        cbr_responce = requests.get(URL_CBR_CURRENCY_BASE_DAILY)
        rates = parse_cbr_currency_base_daily(cbr_responce.text)
        return jsonify(rates)
    except requests.ConnectionError:
        abort(503)


@app.route("/cbr/key_indicators")
def cbr_key_indicators():
    """Function for return result of parsing
    https://www.cbr.ru/eng/key-indicators/"""
    try:
        cbr_responce = requests.get(URL_CBR_KEY_INDICATORS)
        rates = parse_cbr_key_indicators(cbr_responce.text)
        return jsonify(rates)
    except requests.ConnectionError:
        abort(503)


@app.route("/api/asset/add/<char_code>/<name>/<capital>/<interest>")
def add_asset(char_code, name, capital, interest) -> str:
    """Function for add asset in app.bank"""
    capital, interest = float(capital), float(interest)
    if name in app.bank.keys():
        abort(403)
    app.bank[name] = Asset(char_code, name, capital, interest)
    return f"Asset {name} was successfully added", 200


@app.route("/api/asset/list")
def list_asset():
    """Return sorted list of assets in app.bank"""
    list_of_all_asset = [asset.get_params() for asset in app.bank.values()]
    list_of_all_asset = sorted(list_of_all_asset)
    return jsonify(list_of_all_asset)


@app.route("/api/asset/get")
def get_asset():
    """Return sorted list of assets from query"""
    user_query = request.args.getlist("name")
    assets_from_query = [app.bank[name] for name in user_query]
    list_of_assets = [asset.get_params() for asset in assets_from_query]
    list_of_assets = sorted(list_of_assets)
    return jsonify(list_of_assets)


@app.route("/api/asset/calculate_revenue")
def calculate_revenue_asset():
    """Return sum revenue assets from app.bank for periods from query"""
    user_query = request.args.getlist("period")

    cbr_responce = requests.get(URL_CBR_CURRENCY_BASE_DAILY)
    currency_of_daily = parse_cbr_currency_base_daily(cbr_responce.text)

    cbr_responce = requests.get(URL_CBR_KEY_INDICATORS)
    currency_of_key_indicators = parse_cbr_key_indicators(cbr_responce.text)

    revenue = dict()
    for period in user_query:
        sum_revenue = 0
        for asset in app.bank.values():
            if asset.char_code in CHAR_CODES_FOR_KEY_INDICATORS:
                currency = currency_of_key_indicators[asset.char_code]
            elif asset.char_code == "RUB":
                currency = 1
            else:
                currency = currency_of_daily[asset.char_code]
            sum_revenue += currency * asset.calculate_revenue(int(period))
        revenue[period] = sum_revenue

    return jsonify(revenue)


@app.route("/api/asset/cleanup")
def cleanup_asset() -> str:
    """Delete all assets from app.bank"""
    app.bank = dict()
    return "there are no more assets", 200


@app.errorhandler(404)
def page_do_not_exist(error):
    """Exception for 404 error"""
    return "This route is not found", 404


@app.errorhandler(503)
def page_return_503(error):
    """Exception for 503 error"""
    return "CBR service is unavailable", 503


if __name__ == '__main__':
    app.run()
