import itertools # Biblioteca do python escrita em C para lidar com matemática combinatória

# Este script tem o objetivo de criar um arquivo de wordlist que será utilizado em outro script (o de força bruta) e está dividido da seguinte forma:

# 1 - Inputs: Define os blocos de construção da senha.
# É necessário pensar como o alvo: "Quais palavras chave seriam utilizadas como senha de um funcionário da empresa x?"

# 2 - Função geradora: Função responsável por gerar as possíveis senhas
# Utiliza a função de produto cartesiano da lib itertools para gerar as combinações de senha (palavras chave + anos + caracteres especiais)

# 3 - Escrita: Escreve item por item na worlist utilizando o modo de escrita da função open
# Utiliza um for que pede um valor da função geradora até que a última combinação seja entregue e escreve palavra por palavra no arquivo

palavras_base = ["senha", "admin", "teste", "backup", "iago"] # Palavras chave relacionadas ao alvo
numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "123", "12345", "12345678", "123456789"]
sequencias_teclado = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "poiuytrewq", "lkjhgfdsa", "mnbvcxz"]
anos = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
especiais = ["", "!", "@", "#", "."] # Caracteres especiais

nome_arquivo = "custom_wordlist.txt"

def gerador_de_senhas(palavras, anos_chave, nums_chave, seqs_chave, caracteres_especiais):
    """
    Função que gera as possíveis senha a serem escritas no arquivo de wordlists.
    Ao invés de guardar a wordlist inteira na memória para depois escreve-la, 
    ela roda até entregar o yield (a entrega), a escreve no arquivo, apaga da memória 
    e só então gera a segunda entrega, economizando memória RAM.
    :param palavras: lista de palavras chave
    :param anos_chave: lista de anos chave
    :param caracteres_especiais: lista de caracteres especiais
    """
    # Prepara o Produto Cartesiano, combinando todos os itens da lista A com todos os itens da lista B

    # Bloco 1: Anos + Especiais (ex: 2024!)
    sufixos_anos = list(itertools.product(anos_chave, caracteres_especiais))

    # Bloco 2: Números + Especiais (ex: 12345!)
    sufixos_numeros = list(itertools.product(nums_chave, caracteres_especiais))

    # Bloco 3: Sequências + Especiais (ex: qwerty@)
    sufixos_teclado = list(itertools.product(seqs_chave, caracteres_especiais))

    # Juntando todos os blocos numa única lista, evitando gastar performance com 3 loops for
    todos_sufixos = list(itertools.chain(sufixos_anos, sufixos_numeros, sufixos_teclado))

    # loops que usam yield para congelar o estado da função e entregar o valor imediatamente, preservando a memória RAM
    for numero in numeros:
        yield numero
    
    for sequencia in sequencias_teclado:
        yield sequencia
    
    for ano in anos:
        yield ano

    for palavra in palavras:
        # Variações das palavras base (original, capitalizada e upper)
        variacoes_palavra = [palavra, palavra.capitalize(), palavra.upper()]

        for p in variacoes_palavra:
            # Entrega a palavra pura
            yield p

            # Loop que combina a palavra com todos os sufixos
            for complemento, especial in todos_sufixos:
                yield f"{p}{complemento}{especial}"

print(f"[*] Gerando wordlist personalizada em: {nome_arquivo}")

# Escrita segura do arquivo de wordlist. Cria o documento, abre ele em modo de escrita (w) e dá a ele um alias de "f"
with open(nome_arquivo, "w", encoding="utf-8") as f:
    # O with no python funciona como um Context Manager, garantindo que o python fechará o arquivo corretamente caso erros ocorram no meio da escrita

    # Loop para escrever as possíveis senhas no arquivo.
    # O for pede um valor para "senha", chama a funão geradora, a função roda até encontrar o primeiro yield, entrega a senha e congela.
    # O loop, então, pega a senha e a escreve no arquivo.
    for senha in gerador_de_senhas(palavras_base, anos, numeros, sequencias_teclado, especiais):
        f.write(f"{senha}\n")

print(f"[+] Concluído! Verifique o arquivo '{nome_arquivo}'.")
