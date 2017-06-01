
"""
Scrape the webinterface to get various
setup configurations
"""

from bs4 import BeautifulSoup


def _parse_select(select):
    """Get select name and state"""


def _parse_selected(select):
    """Get selected option"""
    option = select.find('option', selected=True)
    return option['value']


def _parse_matrix(matrix):
    """Parse row in audiomatrix"""
    selects = matrix.find_all('select')
    mapping = [(select['name'], _parse_selected(select))
               for select in selects]

    return mapping


def parse_assigned_inputs(html):
    """Parse input assignement matrix from html"""
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    mapping = dict(_parse_matrix(table))

    return mapping

