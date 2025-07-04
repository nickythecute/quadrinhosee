import requests
from bs4 import BeautifulSoup

BASE_URL = "https://readallcomics.com"

def busca_stories(query, max_results=50):
    url = f"{BASE_URL}/?story={query}&s=&type=comic"
    print(f"Buscando em: {url}")
    r = requests.get(url)
    
    if r.status_code != 200:
        print(f"Erro ao acessar o site (Status code: {r.status_code})")
        return []

    soup = BeautifulSoup(r.content, "html.parser")
    resultados = []

    for li in soup.find_all("li"):
        a = li.find("a", href=True, title=True)
        if a:
            href = a.get("href")
            title = a.get("title").strip()
            if href and title and query.lower() in title.lower():
                resultados.append((title, href))
        if len(resultados) >= max_results:
            break

    return resultados

def lista_issues(story_url):
    r = requests.get(story_url)
    soup = BeautifulSoup(r.content, "html.parser")
    issues = []
    for li in soup.find_all("li"):
        a = li.find("a", href=True, title=True)
        if a:
            href = a.get("href")
            title = a.get("title").strip()
            if href and title:
                issues.append((title, href))
    return issues
