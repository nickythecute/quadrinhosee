from search import busca_stories, lista_issues
from download import baixar_images

def main():
    story = input("Digite o termo de busca (Quadrinho): ").strip()
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
