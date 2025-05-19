from itertools import permutations

# Dicionário base
BASE_TRADUCAO = {
    'Physical addresses': 'Endereços físicos',
    'Usernames': 'Nomes de usuário',
    'Passwords': 'Senhas',
    'Email addresses': 'Endereços de e-mail',
    'Phone numbers': 'Números de telefone'
}

def gerar_traducao():
    traducoes = {}
    chaves = list(BASE_TRADUCAO.keys())

    for i in range(1, len(chaves) + 1):
        for p in permutations(chaves, i):
            chave = ', '.join(p)
            valor = ', '.join([BASE_TRADUCAO[c] for c in p])
            traducoes[chave] = valor

 
    traducoes_semicolon = {}
    for chave, valor in traducoes.items():
        chave_sc = chave.replace(', ', '; ')
        valor_sc = valor.replace(', ', '; ')
        traducoes_semicolon[chave_sc] = valor_sc

    traducoes.update(traducoes_semicolon)

    return traducoes


def traduzir_texto_composto(texto, traducoes):
    """
    Traduz um texto composto por termos separados por vírgula ou ponto e vírgula.
    Normaliza a ordem dos termos para garantir que combinações sejam corretamente traduzidas.
    """
    if not texto or not isinstance(texto, str):
        return texto


    if ';' in texto:
        sep = ';'
    else:
        sep = ','


    termos = sorted([t.strip() for t in texto.split(sep)])


    chave_normalizada = (', '.join(termos)).replace(', ', f'{sep} ') if sep == ';' else ', '.join(termos)

    if chave_normalizada in traducoes:
        return traducoes[chave_normalizada]
    

    termos_traduzidos = [traducoes.get(t, t) for t in termos]
    return (sep + ' ').join(termos_traduzidos)