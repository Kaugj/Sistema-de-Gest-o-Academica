"""Funções de entrada de dados: pedem e VALIDAM o que o usuário digita."""


def ler_texto(mensagem):
    """Pede um texto e só aceita se não estiver vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("⚠ Este campo não pode ficar vazio.")


def ler_texto_opcional(mensagem):
    """Pede um texto, mas aceita vazio (usado na atualização: Enter = manter)."""
    return input(mensagem).strip()


def ler_numero(mensagem, minimo, maximo):
    """Pede um número decimal entre minimo e maximo (aceita vírgula ou ponto)."""
    while True:
        bruto = input(mensagem).strip().replace(",", ".")
        try:
            numero = float(bruto)
        except ValueError:
            print("⚠ Digite um número válido (ex.: 7.5).")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"⚠ O valor deve estar entre {minimo} e {maximo}.")


def ler_inteiro(mensagem, minimo=0):
    """Pede um número inteiro maior ou igual a 'minimo'."""
    while True:
        bruto = input(mensagem).strip()
        try:
            numero = int(bruto)
        except ValueError:
            print("⚠ Digite um número inteiro.")
            continue
        if numero >= minimo:
            return numero
        print(f"⚠ O valor deve ser pelo menos {minimo}.")


def confirmar(mensagem):
    """Pergunta sim/não e devolve True ou False."""
    while True:
        resposta = input(f"{mensagem} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("⚠ Responda com 's' ou 'n'.")