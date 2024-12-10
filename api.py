import json
import httpx
import settings as s


base_url = 'https://ser-importacao.vestibulare.com.br/va/api'
chave = s.CHAVE


def unidade():

    params = {
        'chave': chave,
        'acao': 'selecionar'
    }

    response = httpx.get(url=f'{base_url}/unidades.php', params=params)
    response.raise_for_status()
    return response.json()


def turmas(id_unidade: int = 1):
    params = {
        'chave': chave,
        'acao': 'selecionar',
        'idUnidade': id_unidade,
        'tipoTurma': 'cicloComum'
    }

    response = httpx.get(url=f'{base_url}/turmas.php', params=params)
    response.raise_for_status()
    response_json = response.json()

    if not response_json.get('turmas'):
        raise httpx.HTTPStatusError(message=response.text, request=response.request, response=response)

    return response_json


def medias(rota:str, acao: str, rga: str, id_turma: str, periodo: int, ano: int, id_unidade: int = 1):
    params = {
        'chave': chave,
        'acao': acao,
        'emailAdm': 'administrador@vestibulare.com.br',
        'aluno': json.dumps({
            'rga': rga,
            'idTurma': id_turma,
            'idUnidade': id_unidade,
            'periodo': periodo,
            'ano': ano
        })
    }

    response = httpx.get(url=f'{base_url}/{rota}.php', params=params)
    response.raise_for_status()
    response_json = response.json()

    if not response_json.get('resposta'):
        raise httpx.HTTPStatusError(message=response.text, request=response.request, response=response)

    return response_json
