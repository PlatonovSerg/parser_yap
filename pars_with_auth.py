import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://platonov1727.ru/admin/login/?next=/admin/"

if __name__ == "__main__":
    response = requests.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "lxml")
    token = soup.find("input", attrs={"name": "csrfmiddlewaretoken"})["value"]

    data = {
        "username": "platonov",
        "password": "prioritet",
        "csrfmiddlewaretoken": token,
    }