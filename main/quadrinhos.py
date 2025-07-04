import requests
from bs4 import BeautifulSoup
import os

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

def baixar_images(volume_url, pasta="downloads"):
    os.makedirs(pasta, exist_ok=True)
    r = requests.get(volume_url)
    soup = BeautifulSoup(r.content, "html.parser")
    imgs = [img["src"] for img in soup.find_all("img") if img.get("src", "").startswith("http")]
    for i, src in enumerate(imgs, 1):
        try:
            img_data = requests.get(src).content
            path = os.path.join(pasta, f"{volume_url.rstrip('/').split('/')[-1]}_{i:03d}.jpg")
            with open(path, "wb") as f:
                f.write(img_data)
            print(f"Imagem {i} salva: {path}")
        except Exception as e:
            print(f"Falha ao baixar {src}: {e}")

def main():
    story = input("Digite o termo de busca (story): ").strip()
    achados = busca_stories(story)
    if not achados:
        print("Nenhum quadrinho encontrado.")
        return

    print("\nQuadrinhos encontrados:")
    for idx, (t, _) in enumerate(achados, 1):
        print(f"{idx}. {t}")
    sel = int(input("\nEscolha um quadrinho: ")) - 1
    story_url = achados[sel][1]

    issues = lista_issues(story_url)
    if not issues:
        print("Nenhum issue encontrado.")
        return

    print("\nIssues disponíveis:")
    for idx, (t, _) in enumerate(issues, 1):
        print(f"{idx}. {t}")
    
    sel2 = int(input("\nEscolha o issue: ")) - 1
    issue_url = issues[sel2][1]

    baixar_images(issue_url)

if __name__ == "__main__":
    main()
