import requests
import unicodedata

def normalizar_texto(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

def buscar_livros_da_api(categoria):
    url = f"https://openlibrary.org/subjects/{categoria}.json?limit=1" 
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()  
            livros = dados.get("works", [])
            return len(livros) > 0  
        else:
            return False  
    except requests.exceptions.RequestException:
        return False  

def listar_categorias(categorias):
    categorias_disponiveis = {}
    print("\nVerificando disponibilidade de categorias...")

    for chave, nome in categorias.items():
        if buscar_livros_da_api(chave): 
            categorias_disponiveis[chave] = nome + " (disponível)"
        else:
            categorias_disponiveis[chave] = nome + " (indisponível)"

    print("\nAs categorias são:")
    for chave, status in categorias_disponiveis.items():
        print(f"- {status}")
    
    return categorias_disponiveis

def buscar_e_listar_livros(categorias_escolhidas, categorias):
    livros_encontrados = []
    for categoria in categorias_escolhidas:
        print(f"\nBuscando livros da categoria '{categorias[categoria]}'...")
        url = f"https://openlibrary.org/subjects/{categoria}.json?limit=10"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                livros = dados.get("works", [])
                if livros:
                    print(f"\nLivros encontrados na categoria '{categorias[categoria]}':")
                    for i, livro in enumerate(livros, 1):
                        autores = livro.get('authors', [])
                        autor = autores[0]['name'] if autores else 'Autor desconhecido'
                        print(f"{i}. {livro['title']} - {autor}")
                        livros_encontrados.append((livro['title'], autor))
                else:
                    print(f"\nNenhum livro encontrado na categoria '{categorias[categoria]}'.")
            else:
                print(f"\nErro ao acessar a API para a categoria '{categorias[categoria]}'.")
        except requests.exceptions.RequestException:
            print(f"\nErro na requisição para a categoria '{categorias[categoria]}'.")
    
    return livros_encontrados

def main():
    categorias = {
        'fundamental': "Fundamental",
        'infantil': "Infantil",
        'medio': "Médio",
        'programacao': "Programação",
        'ficcao': "Ficção",
        'nao-ficcao': "Não-ficção",
        'historia': "História",
        'literatura': "Literatura",
        'ciencia': "Ciência",
        'arte': "Arte",
        'biografia': "Biografia",
        'tecnologia': "Tecnologia"
    }

    categorias_disponiveis = listar_categorias(categorias)

    while True:
        categorias_escolhidas = input("\nDigite as categorias desejadas separadas por vírgula ou digite 0 para sair: ").strip().lower()
        if categorias_escolhidas == '0':
            print("\nSaindo do programa...")
            return
        
        categorias_escolhidas = [normalizar_texto(cat.strip()) for cat in categorias_escolhidas.split(',')]

        if all(cat in categorias_disponiveis and "disponível" in categorias_disponiveis[cat] for cat in categorias_escolhidas):
            break
        else:
            print("\nErro: Algumas categorias inseridas são inválidas ou indisponíveis. Tente novamente.")

    while True:
        autorizar = input("\nVocê deseja listar os livros encontrados? (s/n): ").strip().lower()
        if autorizar == 's':
            livros_encontrados = buscar_e_listar_livros(categorias_escolhidas, categorias)
            if livros_encontrados:
                print("\nResumo dos livros encontrados:")
                for i, (titulo, autor) in enumerate(livros_encontrados, 1):
                    print(f"{i}. {titulo} - {autor}")
            else:
                print("\nNenhum livro foi encontrado nas categorias selecionadas.")
            break
        elif autorizar == 'n':
            print("\nOperação cancelada. Saindo do programa...")
            break
        else:
            print("\nOpção inválida. Por favor, digite 's' para sim ou 'n' para não.")

if __name__ == "__main__":
    main()
