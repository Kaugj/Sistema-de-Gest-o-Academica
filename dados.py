"""Módulo de DADOS: guarda os estudantes e faz o CRUD
(Create, Read, Update, Delete) + salvar/carregar em arquivo JSON.

Cada estudante é um dicionário:
{
  "matricula": "2024001",
  "nome": "Ana Souza",
  "turma": "A",
  "notas": [8.0, 6.5],
  "aulas_previstas": 40,
  "presencas": 36
}
Todos ficam num dicionário maior, onde a CHAVE é a matrícula.
Assim a busca por matrícula é instantânea e não há matrícula repetida.
"""
import json
import os

ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_academicos.json")

estudantes = {}  # {matricula: dicionário do estudante}


# ---------- CREATE ----------
def cadastrar_estudante(matricula, nome, turma):
    """Cadastra um estudante e devolve False se a matrícula ja existir."""
    if matricula in estudantes:
        return False
    estudantes[matricula] = {
        "matricula": matricula,
        "nome": nome,
        "turma": turma,
        "notas": [],
        "aulas_previstas": 0,
        "presencas": 0,
    }
    return True


# ---------- READ ----------
def buscar_por_matricula(matricula):
    """Devolve o estudante ou None"""
    return estudantes.get(matricula)


def buscar_por_nome(trecho):
    """Busca por parte do nome, sem diferenciar maiúsculas/minúsculas"""
    trecho = trecho.casefold()
    return [e for e in estudantes.values() if trecho in e["nome"].casefold()]


def buscar_por_turma(turma):
    """Devolve todos os estudantes de uma turma"""
    turma = turma.casefold()
    return [e for e in estudantes.values() if e["turma"].casefold() == turma]


def listar_todos():
    return list(estudantes.values())


# ---------- UPDATE ----------
def atualizar_estudante(matricula, nome=None, turma=None):
    """Altera nome e/ou turma. Valor None (ou vazio) = mantém o que já existe."""
    est = estudantes.get(matricula)
    if est is None:
        return False
    if nome:
        est["nome"] = nome
    if turma:
        est["turma"] = turma
    return True


def adicionar_nota(matricula, nota):
    est = estudantes.get(matricula)
    if est is None:
        return False
    est["notas"].append(nota)
    return True


def remover_nota(matricula, posicao):
    """Remove a nota na posição (0 = primeira). Devolve False se não existir."""
    est = estudantes.get(matricula)
    if est is None or not (0 <= posicao < len(est["notas"])):
        return False
    est["notas"].pop(posicao)
    return True


def registrar_aulas(matricula, aulas, presencas):
    """SOMA aulas previstas e presenças ao que já existe."""
    est = estudantes.get(matricula)
    if est is None or presencas > aulas:
        return False
    est["aulas_previstas"] += aulas
    est["presencas"] += presencas
    return True


# ---------- DELETE ----------
def remover_estudante(matricula):
    return estudantes.pop(matricula, None) is not None


# ---------- PERSISTÊNCIA ----------
def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(estudantes, f, ensure_ascii=False, indent=2)


def carregar():
    """Lê o arquivo, se existir. Se estiver corrompido, começa vazio"""
    estudantes.clear()
    if not os.path.exists(ARQUIVO):
        return
    try:
        with open(ARQUIVO, encoding="utf-8") as f:
            estudantes.update(json.load(f))
    except (json.JSONDecodeError, OSError):
        print("⚠ Não consegui ler o arquivo de dados; começando vazio")