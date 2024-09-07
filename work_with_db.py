import requests
from bs4 import BeautifulSoup
from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    insert,
    select,
    update,
)
from sqlalchemy.orm import Session, declarative_base, declared_attr

PEP_URL = "https://peps.python.org/#numerical-index"


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class Pep(Base):
    number = Column(Integer, unique=True)
    title = Column(String(200))
    type_status = Column(String(2))
    authors = Column(String(200))

    def __repr__(self):
        return f"Pep {self.pep_number}, {self.name}"


if __name__ == "__main__":
    engine = create_engine("sqlite:///sqlite.db")
    Base.metadata.create_all(engine)
    session = Session(engine)

    def parse_pep_add_to_bd():
        response = requests.get(PEP_URL)
        soup = BeautifulSoup(response.text, features="lxml")
        section_tag = soup.find("section", attrs={"id": "numerical-index"})
        tbody_tag = section_tag.find("tbody")
        tr_tags = tbody_tag.find_all("tr")
        for tr_tag in tr_tags:
            type_status = tr_tag.find("td").text
            number = tr_tag.find("td").find_next_sibling().text
            title = (
                tr_tag.find("td").find_next_sibling().find_next_sibling().text
            )
            authors = (
                tr_tag.find("td")
                .find_next_sibling()
                .find_next_sibling()
                .find_next_sibling()
                .text
            )
            pep = Pep(
                number=number,
                title=title,
                type_status=type_status,
                authors=authors,
            )
            session.add(pep)
        session.commit()
