"""Módulo de REGRAS: todos os cálculos e classificações.
Não imprime nada e não pede nada ao usuário: só recebe dados e devolve resultados.
Isso facilita testar e reaproveitar."""

MEDIA_APROVACAO = 7.0
MEDIA_RECUPERACAO = 5.0
FREQUENCIA_MINIMA = 75.0


def calcular_media(est):
    """Média aritmética das notas. Sem notas -> None."""
    if not est["notas"]:
        return None
    return sum(est["notas"]) / len(est["notas"])


def calcular_frequencia(est):
    """Percentual de presença. Sem aulas registradas -> None."""
    if est["aulas_previstas"] == 0:
        return None
    return est["presencas"] / est["aulas_previstas"] * 100


def classificar_media(media):
    """Aplica a regra de referência do enunciado."""
    if media is None:
        return "Sem notas"
    if media >= MEDIA_APROVACAO:
        return "Aprovado"
    if media >= MEDIA_RECUPERACAO:
        return "Recuperação"
    return "Reprovado"


def frequencia_insuficiente(est):
    freq = calcular_frequencia(est)
    return freq is not None and freq < FREQUENCIA_MINIMA


def situacao_final(est):
    """Combina nota e frequência. Frequência abaixo de 75% reprova por falta,
    mesmo com média alta."""
    if frequencia_insuficiente(est):
        return "Reprovado por frequência"
    return classificar_media(calcular_media(est))


def ordenar_por_media(lista):
    """Do maior para o menor. Quem não tem média vai para o final."""
    com_media = [e for e in lista if calcular_media(e) is not None]
    sem_media = [e for e in lista if calcular_media(e) is None]
    com_media.sort(key=calcular_media, reverse=True)
    return com_media + sem_media


def contar_situacoes(lista):
    """Devolve {'Aprovado': n, 'Recuperação': n, 'Reprovado': n, ...}."""
    contagem = {}
    for est in lista:
        s = situacao_final(est)
        # "Reprovado por frequência" também conta como Reprovado no total geral
        s = "Reprovado" if s.startswith("Reprovado") else s
        contagem[s] = contagem.get(s, 0) + 1
    return contagem


def maior_e_menor_media(lista):
    """Devolve (estudante de maior média, estudante de menor média) ou (None, None)."""
    com_media = [e for e in lista if calcular_media(e) is not None]
    if not com_media:
        return None, None
    return (max(com_media, key=calcular_media),
            min(com_media, key=calcular_media))


def nomes_em_turmas_diferentes(lista):
    """Nomes que aparecem em 2 ou mais turmas, SEM repetir resultados.
    Usa um dicionário de conjuntos: nome -> {turmas}. Como conjunto (set) não
    guarda repetidos, o mesmo nome/turma nunca é contado duas vezes."""
    mapa = {}
    for est in lista:
        chave = est["nome"].strip().casefold()
        mapa.setdefault(chave, {"nome": est["nome"], "turmas": set()})
        mapa[chave]["turmas"].add(est["turma"].upper())
    return {
        v["nome"]: sorted(v["turmas"])
        for v in mapa.values() if len(v["turmas"]) >= 2
    }


def alunos_em_acompanhamento(lista, criterio="ambos"):
    """Estudantes que precisam de acompanhamento.
    criterio: 'nota' (média < 7), 'frequencia' (< 75%) ou 'ambos' (um OU outro)."""
    resultado = []
    for est in lista:
        media = calcular_media(est)
        problema_nota = media is not None and media < MEDIA_APROVACAO
        problema_freq = frequencia_insuficiente(est)
        if ((criterio == "nota" and problema_nota)
                or (criterio == "frequencia" and problema_freq)
                or (criterio == "ambos" and (problema_nota or problema_freq))):
            resultado.append(est)
    return resultado