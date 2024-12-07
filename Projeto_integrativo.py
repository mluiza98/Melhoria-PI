import requests
import unicodedata

def normalizar_texto(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))


def buscar_livros_da_api(categoria):
    url = f"https://openlibrary.org/subjects/{categoria}.json?limit=10"
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()  
            livros = dados.get("works", [])
            
            if livros:
                print(f"\nLivros encontrados na categoria '{categoria}':")
                for i, livro in enumerate(livros, 1):
                    autores = livro.get('authors', [])
                    autor = autores[0]['name'] if autores else 'Autor desconhecido'
                    print(f"{i}. {livro['title']} - {autor}")
                return livros  
            else:
                print("Nenhum livro encontrado para essa categoria.")
                return [] 
        else:
            print(f"Erro ao acessar a API: {response.status_code}")
            return []  
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []  


def validar_entrada(entrada, max_valor):
    try:
        valores = [int(num.strip()) for num in entrada.split(',')]
        
        if all(1 <= num <= max_valor for num in valores):
            return valores
        elif entrada.strip() == '0':  
            return 'sair'
        else:
            print(f"Por favor, insira números entre 1 e {max_valor}, ou 0 para sair.")
            return None
    except ValueError:
        print("Entrada inválida. Por favor, insira apenas números inteiros.")
        return None


def exibir_e_selecionar_livros():
    livros_selecionados = {'fundamental': [], 'medio': [], 'programacao': [], 'infantil': [],
                           'ficcao': [], 'nao-ficcao': [], 'historia': [], 'literatura': [],
                           'ciencia': [], 'arte': [], 'biografia': [], 'tecnologia': []}
    
    while True:
        ver_livros = input("Deseja ver uma lista dos livros disponíveis para qual tipo de ensino ou tema (Fundamental, Médio, Programação, Infantil, Ficção, História, Ciência, Arte, Biografia, Tecnologia)? Ou digite 0 para sair: ").strip().lower()
        
        if ver_livros == '0': 
            break
        
        ver_livros_normalizado = normalizar_texto(ver_livros)  
        
        if ver_livros_normalizado == 'fundamental':
            categoria = 'fundamental'
        elif ver_livros_normalizado == 'medio':
            categoria = 'medio'
        elif ver_livros_normalizado == 'programacao':
            categoria = 'programacao'
        elif ver_livros_normalizado == 'infantil':
            categoria = 'infantil'
        elif ver_livros_normalizado == 'ficcao':
            categoria = 'ficcao'
        elif ver_livros_normalizado == 'nao-ficcao':
            categoria = 'nao-ficcao'
        elif ver_livros_normalizado == 'historia':
            categoria = 'historia'
        elif ver_livros_normalizado == 'literatura':
            categoria = 'literatura'
        elif ver_livros_normalizado == 'ciencia':
            categoria = 'ciencia'
        elif ver_livros_normalizado == 'arte':
            categoria = 'arte'
        elif ver_livros_normalizado == 'biografia':
            categoria = 'biografia'
        elif ver_livros_normalizado == 'tecnologia':
            categoria = 'tecnologia'
        else:
            print("Categoria inválida! Tente novamente.")
            continue
        
        livros = buscar_livros_da_api(categoria)
        
        if livros:
            escolha_livros = input('Com base na tabela, selecione os itens que você deseja baixar (separados por vírgula) ou digite "0" para sair: ')
            num_escolhidos = validar_entrada(escolha_livros, len(livros)) 
            
            if num_escolhidos == 'sair':
                break

            if num_escolhidos:
                for c in num_escolhidos:
                    livro_selecionado = livros[c - 1]
                    livros_selecionados[categoria].append(livro_selecionado['title'])
                    print(f"Você escolheu o livro: {livro_selecionado['title']}")

    print("\nLista de livros escolhidos por categoria:")
    for categoria, livros in livros_selecionados.items():
        if livros:
            print(f"\nCategoria {categoria.capitalize()}:")
            for livro in livros:
                print(f"- {livro}")


def main():
    exibir_e_selecionar_livros()


if __name__ == "__main__":
    main()
