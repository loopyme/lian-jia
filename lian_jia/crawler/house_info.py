from bs4 import BeautifulSoup


def _extract_basic_info(soup: BeautifulSoup):
    soup.select('.introContent .content .label')
