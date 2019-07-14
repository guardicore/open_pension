import os
import requests
from bs4 import BeautifulSoup

base_url = "http://infinity.co.il/nihulkupot/Kahar/%D7%A7-%D7%94-%D7%A8-%D7%A0%D7%9B%D7%A1%D7%99-%D7%94%D7%A7%D7%95%D7%A4%D7%94-%D7%95%D7%AA%D7%A9%D7%95%D7%90%D7%95%D7%AA/%D7%A7-%D7%94-%D7%A8-%D7%A8%D7%A9%D7%99%D7%9E%D7%AA-%D7%A0%D7%9B%D7%A1%D7%99%D7%9D-%D7%A8%D7%91%D7%A2%D7%95%D7%A0%D7%99%D7%AA/"

report_text_base = "דוח נכסים רבעון"

report_text_template = '{base} {quarter} {year}'

save_path = '/tmp/reports'


def get_khr_quarterly(year, quarter):
    """
    ק.ה.ר - קרן השתלמות לרוקחים בע"מ
    :param year:
    :param quarter:
    :return:
    """
    r = requests.get(base_url)
    parsed_html = BeautifulSoup(r.content)
    report_text_by_year_month = report_text_template.format(base=report_text_base,
                                                            year=year,
                                                            quarter=quarter)
    items = parsed_html.find_all(text=report_text_by_year_month)
    if not items:
        print(f"Failed finding report for {year}-{quarter}")
        return

    p = items[0].parent
    href = p['href']

    d = requests.get(href)

    file_path = os.path.join(save_path, f'{year}-{quarter}.xls')
    with open(file_path, 'wb') as f:
        f.write(d.content)
        print(f'Saved file {href} to {file_path}')


if __name__ == '__main__':
    get_khr_quarterly(2017, 4)




