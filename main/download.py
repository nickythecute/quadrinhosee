import requests
import os
from bs4 import BeautifulSoup

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
