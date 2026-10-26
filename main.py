"""Módulo PRINCIPAL: menu e fluxo do programa.
   Só conversa com o usuário e chama os outros módulos."""
import dados
import regras
import relatorios
from utils import (ler_texto, ler_texto_opcional, ler_numero,
                   ler_inteiro, confirmar)

MENU = """
========== SISTEMA DE GESTÃO ACADÊMICA ==========
 1 - Cadastrar estudante
 2 - Consultar estudantes
 3 - Atualizar estudante
 4 - Remover estudante
 5 - Lançar / remover avaliações
 6 - Registrar aulas e presenças
 7 - Relatório individual
 8 - Relatório geral
 9 - Classificação por média
10 - Estudantes em acompanhamento
11 - Nomes em turmas diferentes
 0 - Encerrar
=================================================="""


def pedir_estudante():
    """Pede a matrícula e devolve o estudante (ou None, avisando)."""
    matricula = ler_texto("Matrícula: ")
    est = dados.buscar_por_matricula(matricula)
    if est is None:
        print("⚠ Matrícula não encontrada.")
    return est


def opcao_cadastrar():
    matricula = ler_texto("Matrícula: ")
    if dados.buscar_por_matricula(matricula):
        print("⚠ Já existe estudante com esta matrícula.")
        return False
    nome = ler_texto("Nome completo: ")
    turma = ler_texto("Turma: ").upper()
    dados.cadastrar_estudante(matricula, nome, turma)
    print("✔ Estudante cadastrado!")
    return True


def opcao_consultar():
    print("Consultar por: 1-Matrícula  2-Nome  3-Turma  4-Todos")
    tipo = ler_inteiro("Opção: ", 1)
    if tipo == 1:
        est = dados.buscar_por_matricula(ler_texto("Matrícula: "))
        resultado = [est] if est else []
    elif tipo == 2:
        resultado = dados.buscar_por_nome(ler_texto("Nome (ou parte): "))
    elif tipo == 3:
        resultado = dados.buscar_por_turma(ler_texto("Turma: "))
    elif tipo == 4:
        resultado = dados.listar_todos()
    else:
        print("⚠ Opção inválida.")
        return
    if not resultado:
        print("Nenhum estudante encontrado.")
    for est in resultado:
        print(relatorios.linha_estudante(est))


def opcao_atualizar():
    est = pedir_estudante()
    if est is None:
        return False
    print(f"Atual: {est['nome']} / Turma {est['turma']} (Enter mantém o valor)")
    nome = ler_texto_opcional("Novo nome: ")
    turma = ler_texto_opcional("Nova turma: ").upper()
    dados.atualizar_estudante(est["matricula"], nome, turma)
    print("✔ Dados atualizados!")
    return True


def opcao_remover():
    est = pedir_estudante()
    if est is None:
        return False
    if confirmar(f"Remover {est['nome']}?"):
        dados.remover_estudante(est["matricula"])
        print("✔ Estudante removido.")
        return True
    print("Operação cancelada.")
    return False


def opcao_notas():
    est = pedir_estudante()
    if est is None:
        return False
    print(f"Notas atuais: {est['notas'] or 'nenhuma'}")
    print("1 - Adicionar avaliações   2 - Remover uma avaliação")
    escolha = ler_inteiro("Opção: ", 1)
    if escolha == 1:
        while True:  # permite várias avaliações seguidas
            nota = ler_numero("Nota (0 a 10): ", 0, 10)
            dados.adicionar_nota(est["matricula"], nota)
            if not confirmar("Lançar outra avaliação?"):
                break
        print("✔ Notas registradas!")
        return True
    if escolha == 2 and est["notas"]:
        pos = ler_inteiro(f"Número da avaliação (1 a {len(est['notas'])}): ", 1)
        if dados.remover_nota(est["matricula"], pos - 1):
            print("✔ Avaliação removida.")
            return True
        print("⚠ Número inexistente.")
    return False


def opcao_aulas():
    est = pedir_estudante()
    if est is None:
        return False
    aulas = ler_inteiro("Quantas aulas foram previstas (a somar)? ", 1)
    while True:
        presencas = ler_inteiro("Em quantas o estudante esteve presente? ", 0)
        if presencas <= aulas:
            break
        print("⚠ Presenças não podem superar as aulas previstas.")
    dados.registrar_aulas(est["matricula"], aulas, presencas)
    freq = regras.calcular_frequencia(est)
    print(f"✔ Registrado! Frequência atual: {freq:.1f}%")
    if regras.frequencia_insuficiente(est):
        print("⚠ ATENÇÃO: frequência abaixo de 75%.")
    return True


def opcao_relatorio_individual():
    est = pedir_estudante()
    if est:
        print(relatorios.relatorio_individual(est))


def opcao_acompanhamento():
    print("Critério: 1-Nota  2-Frequência  3-Ambos")
    criterio = {1: "nota", 2: "frequencia", 3: "ambos"}.get(ler_inteiro("Opção: ", 1))
    if criterio is None:
        print("⚠ Opção inválida.")
        return
    print(relatorios.lista_acompanhamento(dados.listar_todos(), criterio))


def main():
    dados.carregar()
    while True:                      # repete até o usuário escolher 0
        print(MENU)
        opcao = ler_inteiro("Escolha uma opção: ", 0)
        alterou = False              # só salva no arquivo se algo mudou
        if opcao == 1:
            alterou = opcao_cadastrar()
        elif opcao == 2:
            opcao_consultar()
        elif opcao == 3:
            alterou = opcao_atualizar()
        elif opcao == 4:
            alterou = opcao_remover()
        elif opcao == 5:
            alterou = opcao_notas()
        elif opcao == 6:
            alterou = opcao_aulas()
        elif opcao == 7:
            opcao_relatorio_individual()
        elif opcao == 8:
            print(relatorios.relatorio_geral(dados.listar_todos()))
        elif opcao == 9:
            print(relatorios.ranking(dados.listar_todos()))
        elif opcao == 10:
            opcao_acompanhamento()
        elif opcao == 11:
            print(relatorios.lista_nomes_repetidos(dados.listar_todos()))
        elif opcao == 0:
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("⚠ Opção inválida.")
        if alterou:
            dados.salvar()


if __name__ == "__main__":
    main()