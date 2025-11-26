import sys
import time
import os
import multiprocessing
from multiprocessing import Pool, cpu_count
import pikepdf

try:
    multiprocessing.set_start_method('spawn') # Altera o método de inicialização do multiprocessing para spawn, que é mais seguro e compatível com libs C++
except RuntimeError:
    pass

# CONFIGURAÇÕES
PDF_ALVO = "teste_protegido.pdf"      # Nome do arquivo PDF alvo
WORDLIST = "custom_wordlist.txt"     # Nome da sua wordlist

def testar_senha(args):
    """
    Função Worker que será executada em paralelo por cada núcleo da CPU.
    Recebe o caminho do arquivo e a senha da wordlist a ser testada.
    """
    arquivo_pdf, senha = args
    try:
        # Tenta abrir o PDF com a senha fornecida
        with pikepdf.open(arquivo_pdf, password=senha): # pikepdf.open faz a validação matemática do hash internamente, testando a senha fornecida para o arquivo alvo
            # Se não der erro, a senha está correta, então é retornada
            return senha
    except pikepdf.PasswordError:
        # Senha incorreta, segue o jogo
        return None

def carregar_wordlist(caminho_wordlist):
    """
    Gerador para ler o arquivo linha por linha (Lazy Loading).
    Evita carregar arquivos de 10GB na RAM de uma vez.
    """
    if not os.path.exists(caminho_wordlist):
        print(f"[!] Erro: Wordlist '{caminho_wordlist}' não encontrada.")
        sys.exit(1)
        
    with open(caminho_wordlist, 'r', encoding='latin-1', errors='ignore') as f:
        for linha in f:
            yield linha.strip()

def main():
    if not os.path.exists(PDF_ALVO):
        print(f"[!] Erro: Arquivo alvo '{PDF_ALVO}' não encontrado.")
        return

    print(f"[*] Iniciando ataque contra: {PDF_ALVO}")
    print(f"[*] Usando {cpu_count()} núcleos de processamento...")
    
    inicio = time.time()
    senha_encontrada = None
    
    # Prepara os argumentos (tuplas) para passar para os processos
    # Isso combina o nome do arquivo com cada senha da wordlist
    tarefas = ((PDF_ALVO, senha) for senha in carregar_wordlist(WORDLIST))

    # Cria um pool de processos igual ao número de núcleos da CPU
    with Pool(processes=cpu_count()) as pool:
        # imap_unordered distribui as tarefas e processa assim que elas terminam
        # chunksize define quantas senhas cada processo pega por vez
        for resultado in pool.imap_unordered(testar_senha, tarefas, chunksize=50):
            if resultado:
                senha_encontrada = resultado
                pool.terminate() # Para todos os outros processos imediatamente
                break
    
    fim = time.time()
    
    if senha_encontrada:
        print(f"\n Senha encontrada: {senha_encontrada}")
        print(f"[*] Tempo decorrido: {fim - inicio:.2f} segundos")
    else:
        print("\n[FALHA] A senha não está na wordlist fornecida.")

if __name__ == "__main__":
    main()