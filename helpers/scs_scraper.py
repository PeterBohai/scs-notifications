import requests
from bs4 import BeautifulSoup


def extract_swagcode(url):
    """Gets Swag Code information from a sc-s.com page by scraping the page HTML content.

    Args:
        url (str): The sc-s.com page URL that contains the newest Swag Code information.

    Returns:
        dict: Contains Swag Code information such as 'type' and 'value'. The 'type' field can be 'static' or 'dynamic'.

    """
    res = {
        'type': None,
        'value': None
    }

    source_text = requests.get(url).text
    soup = BeautifulSoup(source_text, 'html.parser')

    post_content_table = soup.article.find('table')
    table_trs = post_content_table.find_all('tr')

    # Look for the row that has the "Swag Code" td label
    swagcode_value_td = None
    for tr in table_trs:
        td_label = tr.find_next('td', class_='p_label').string
        if 'swag code' in td_label.lower():
            swagcode_value_td = tr.select('td.p_value.p_code')[0]
            break

    if not swagcode_value_td:
        print('No Swag Code row in the post!')
        return res

    dynamic_swagcode_anchor = swagcode_value_td.find_next('a', class_='p_dynamic_code_link')
    if dynamic_swagcode_anchor:
        dynamic_swagcode_text = dynamic_swagcode_anchor.string
        dynamic_swagcode_url = dynamic_swagcode_anchor['href']
        res['type'] = 'dynamic'
        res['value'] = dynamic_swagcode_url
    else:
        # The Swag Code is just the inner text of the <td> element if it's not a dynamic code
        static_swagcode_val = swagcode_value_td.string
        res['type'] = 'static'
        res['value'] = static_swagcode_val

    return res


if __name__ == '__main__':
    print(extract_swagcode('https://sc-s.com/2021/05/19/35472/'))
    print(extract_swagcode('https://sc-s.com/2021/05/18/35463/'))
