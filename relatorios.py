"""Módulo de RELATÓRIOS: transforma dados e resultados em texto formatado.
Cada função DEVOLVE uma string; quem imprime é o menu."""
import regras

LINHA = "=" * 56


def _fmt(valor, sufixo=""):
    return "—" if valor is None else f"{valor:.1f}{sufixo}"


def linha_estudante(est):
    """Uma linha resumida (usada em listas e consultas)."""
    return (f"{est['matricula']:<10} {est['nome']:<24} Turma {est['turma']:<4} "
            f"Média: {_fmt(regras.calcular_media(est)):>4}")


def relatorio_individual(est):
    media = regras.calcular_media(est)
    freq = regras.calcular_frequencia(est)
    notas = ", ".join(f"{n:.1f}" for n in est["notas"]) or "nenhuma"
    return "\n".join([
        LINHA,
        "RELATÓRIO INDIVIDUAL",
        LINHA,
        f"Matrícula : {est['matricula']}",
        f"Nome      : {est['nome']}",
        f"Turma     : {est['turma']}",
        f"Avaliações: {notas}",
        f"Média     : {_fmt(media)}",
        f"Aulas     : {est['presencas']} presenças de {est['aulas_previstas']} previstas",
        f"Frequência: {_fmt(freq, '%')}",
        f"Situação  : {regras.situacao_final(est)}",
        LINHA,
    ])


def relatorio_geral(lista):
    contagem = regras.contar_situacoes(lista)
    maior, menor = regras.maior_e_menor_media(lista)
    linhas = [
        LINHA, "RELATÓRIO GERAL", LINHA,
        f"Total de estudantes : {len(lista)}",
        f"Aprovados           : {contagem.get('Aprovado', 0)}",
        f"Em recuperação      : {contagem.get('Recuperação', 0)}",
        f"Reprovados          : {contagem.get('Reprovado', 0)}",
        f"Sem notas           : {contagem.get('Sem notas', 0)}",
    ]
    if maior:
        linhas.append(f"Maior média         : {regras.calcular_media(maior):.1f} ({maior['nome']})")
        linhas.append(f"Menor média         : {regras.calcular_media(menor):.1f} ({menor['nome']})")
    else:
        linhas.append("Maior/menor média   : sem notas lançadas")
    linhas.append(LINHA)
    return "\n".join(linhas)


def ranking(lista):
    linhas = [LINHA, "CLASSIFICAÇÃO ACADÊMICA (por média)", LINHA]
    for pos, est in enumerate(regras.ordenar_por_media(lista), start=1):
        linhas.append(f"{pos:>2}º {est['nome']:<24} Turma {est['turma']:<4} "
                      f"Média: {_fmt(regras.calcular_media(est)):>4}")
    return "\n".join(linhas)


def lista_acompanhamento(lista, criterio):
    titulos = {"nota": "por NOTA (média < 7,0)",
               "frequencia": "por FREQUÊNCIA (< 75%)",
               "ambos": "por NOTA ou FREQUÊNCIA"}
    linhas = [LINHA, f"ACOMPANHAMENTO {titulos[criterio]}", LINHA]
    alunos = regras.alunos_em_acompanhamento(lista, criterio)
    if not alunos:
        linhas.append("Nenhum estudante nesta condição.")
    for est in alunos:
        linhas.append(f"{est['nome']:<24} Turma {est['turma']:<4} "
                      f"Média: {_fmt(regras.calcular_media(est)):>4}  "
                      f"Freq: {_fmt(regras.calcular_frequencia(est), '%'):>6}")
    return "\n".join(linhas)


def lista_nomes_repetidos(lista):
    repetidos = regras.nomes_em_turmas_diferentes(lista)
    linhas = [LINHA, "NOMES EM TURMAS DIFERENTES", LINHA]
    if not repetidos:
        linhas.append("Nenhum nome aparece em mais de uma turma.")
    for nome, turmas in repetidos.items():
        linhas.append(f"{nome}: turmas {', '.join(turmas)}")
    return "\n".join(linhas)