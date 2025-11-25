import itertools # Biblioteca padrão do python para lidar com matemática combinatória

# Configurações do Alvo
palavras_base = ["12345", "senha", "admin", "techcorp", "teste", "backup", "financeiro"] # Palavras chave relacionadas ao alvo
anos = ["2023", "2024", "2025"] # Todos os anos em que a empresa esteve ativa
especiais = ["", "!", "@", "#", "123"] # Caracteres especiais que podem ser utilizados

nome_arquivo = "custom_wordlist.txt"

def gerador_de_senhas(palavras, anos, caracteres_especiais):
    """
    Função geradora (Generator).
    Em vez de return, usa yield para entregar uma senha de cada vez.
    Ao invés de guardar a wordlist inteira na memória para depois escreve-la, ela roda até entregar o yield (a entrega), a escreve no arquivo, apaga da memória e só então gera a segunda entrega.
    Isso economiza memória RAM, pois a lista completa nunca é criada na memória.
    """
    
    # Prepara o Produto Cartesiano dos anos e caracteres especiais
    # O itertools.product substitui os loops "for" aninhados (nested loops), criando todas as combinações de (Ano + Especial) automaticamente
    sufixos = list(itertools.product(anos, caracteres_especiais))
    
    for palavra in palavras:
        # Entrega as palavras base puras e capitalizadas
        yield f"{palavra}" 
        yield f"{palavra.capitalize()}"
        
        # Gera as combinações complexas usando o sufixo pré-calculado e combinando ele com as palavras base
        for ano, especial in sufixos:
            # F-strings são preferidas em ataque pois são processadas mais rapidamente pelo interpretador e são melhores para montar strings dinâmicas
            
            # Variação minúscula
            yield f"{palavra}{ano}{especial}"
            
            # Variação Capitalizada
            yield f"{palavra.capitalize()}{ano}{especial}"

print(f"[*] Gerando wordlist personalizada em: {nome_arquivo}")

### Cria o documento {nome_arquivo}, abre ele em modo de escrita (W) e dá a ele um alias de "f"
with open(nome_arquivo, "w") as f:
    # O with no python funciona como um Context Manager, garantindo que o python fechará o arquivo corretamente, garantindo segurança operacional
    
    # O loop pede uma senha, o gerador cria ELA SOZINHA,
    # o script escreve no arquivo e a descarta da memória imediatamente.
    for senha in gerador_de_senhas(palavras_base, anos, especiais):
        f.write(f"{senha}\n")

print(f"[+] Concluído! Verifique o arquivo '{nome_arquivo}'.")