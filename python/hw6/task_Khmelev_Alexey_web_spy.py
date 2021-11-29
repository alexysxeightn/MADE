""" Script for spy Gitlab.com """
import sys
import requests
from bs4 import BeautifulSoup

URL_GITLAB = 'https://about.gitlab.com/features/'
TITLE_OF_FREE_PRODUCTS = "Available in GitLab SaaS Free"
TITLE_OF_ENTERPRISE_PRODUCTS = "Not available in SaaS Free"


def process_for_gitlab(url_gitlab):
    """ Return number of products on Gitlab.com """
    gitlab_html = requests.get(url_gitlab)
    gitlab_html = gitlab_html.text
    gitlab_soup = BeautifulSoup(gitlab_html, features='html.parser')

    links_on_free_products = gitlab_soup.find_all(
        "a", attrs={"title": TITLE_OF_FREE_PRODUCTS}
    )
    links_on_enterprise_products = gitlab_soup.find_all(
        "a", attrs={"title": TITLE_OF_ENTERPRISE_PRODUCTS}
    )

    num_free_products = len(links_on_free_products)
    num_enterprise_products = len(links_on_enterprise_products)

    return num_free_products, num_enterprise_products


def print_result_gitlab():
    """ Print result of process_for_gitlab """
    num_free_products, num_enterprise_products = process_for_gitlab(URL_GITLAB)
    print(f'free products: {num_free_products}')
    print(f'enterprise products: {num_enterprise_products}')


if __name__ == "__main__":
    if 'gitlab' in sys.argv and len(sys.argv) == 2:
        print_result_gitlab()
