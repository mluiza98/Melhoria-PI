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

        indisponiveis = [cat for cat in categorias_escolhidas if cat not in categorias_disponiveis or "indisponível" in categorias_disponiveis[cat]]
        validas = [cat for cat in categorias_escolhidas if cat in categorias_disponiveis and "disponível" in categorias_disponiveis[cat]]

        if indisponiveis:
            print("\nAs seguintes categorias são indisponíveis ou inválidas:")
            for cat in indisponiveis:
                print(f"- {cat}")
            tentar_novamente = input("\nDeseja selecionar outra categoria? (s/n): ").strip().lower()
            if tentar_novamente == 'n':
                print("\nSaindo do programa...")
                return
            else:
                continue

        if validas:
            print("\nListando livros das categorias válidas selecionadas...")
            buscar_e_listar_livros(validas, categorias)

        continuar = input("\nVocê deseja buscar mais categorias? (s/n): ").strip().lower()
        if continuar == 'n':
            print("\nSaindo do programa...")
            return

if __name__ == "__main__":
    main()
