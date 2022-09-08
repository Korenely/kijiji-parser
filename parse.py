import re
import requests
import dateparser
from bs4 import BeautifulSoup
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

NAMBER_OF_PAGES = 94

meta = MetaData()

kijiji_elements = Table(
   'kijiji_elements', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('description', String),
    Column('location', String),
    Column('image', String),
    Column('date', String),
    Column('beds', Integer),
    Column('currency', String),
    Column('price', String),
)

engine = create_engine("postgresql://kbnlfbzg:tuDebiXJdcPwyBGOXmPs04QqFaXrzFsH@abul.db.elephantsql.com/kbnlfbzg") # HARDCODE IS NOT SECURE
meta.create_all(engine)


def parse_single_element(element_soup: BeautifulSoup):
    conn = engine.connect()

    try:
        beds = int(re.findall("\d+", element_soup.select_one(".beds").text.strip())[0])
    except IndexError:
        beds = 0

    description = element_soup.select_one(".description").text.strip().replace("\n", "").replace("  ", "")
    date = dateparser.parse(element_soup.select_one(".date-posted").text.strip()).strftime("%d-%m-%Y")

    kijiji_elements_add = kijiji_elements.insert().values(
        title=element_soup.select_one(".title").text.strip(),
        description=description,
        location=element_soup.select_one(".location > span").text.strip(),
        image=element_soup.select_one("img")["src"].strip(),
        date=date,
        beds=beds,
        currency=element_soup.select_one(".price").text.strip()[0].strip(),
        price=element_soup.select_one(".price").text.strip()[1:],
    )
    conn.execute(kijiji_elements_add)


def main():
    i = 0
    while i < NAMBER_OF_PAGES:
        i = i + 1
        page = requests.get(f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i}/c37l1700273").content
        soup = BeautifulSoup(page, "html.parser")
        elements = soup.select(".top-feature")
        return [parse_single_element(element_soup) for element_soup in elements]


if __name__ == "__main__":
    main()