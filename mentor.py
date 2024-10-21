import httpx
import settings as s


base_url = s.MENTOR_URL
usuario = s.MENTOR_USER
senha = s.MENTOR_PASSWORD


def gera_token(servico):
    url = f'{base_url}/rest/servicoexterno/token/{servico}'

    headers = {
        'usuario': usuario,
        'senha': senha
    }

    response = httpx.get(url=url, headers=headers, timeout=10)

    if response.status_code != 200:
        raise httpx.HTTPStatusError(message=response.text, request=response.request, response=response)

    return response.text # token


def grava_nota(id_avaliacao: int, id_aluno: int, nota: str):
    servico = 'gravaNotaAvaliacao'

    url = f'{base_url}/rest/servicoexterno/execute/{servico}'

    headers = {
        'token': gera_token(servico)
    }

    payload = {
        'idAvaliacao': id_avaliacao,
        'listAlunoNota': [
            {
                'idAluno': id_aluno,
                'nota': nota
            }
        ]
    }

    response = httpx.post(url=url, headers=headers, json=payload, timeout=15)

    if response.status_code != 200:
        raise httpx.HTTPStatusError(message=response.text, request=response.request, response=response)

    return response.json()


def lanca_falta(cod_turma, cod_disciplina, ra, data_falta):
    servico = 'insereFalta'

    url = f'{base_url}/rest/servicoexterno/execute/{servico}'

    headers = {
        'token': gera_token(servico)
    }

    payload = {
        'INSERE_FALTAS': [
            {
                'Cod_turma': cod_turma,
                'Cod_discip': cod_disciplina,
                'Cod_aluno': ra,
                'Data_falta': data_falta
            }
        ],
        'ATUALIZA_CRONOGRAMA': [
            {
                'Cod_turma': cod_turma,
                'Cod_discip': cod_disciplina,
                'Data_falta': data_falta
            }
        ],
        'ATUALIZA_HISTORICO': [
            {
                'Cod_turma': cod_turma,
                'Cod_discip': cod_disciplina,
                'Cod_aluno': ra
            }
        ]
    }

    response = httpx.post(url=url, headers=headers, json=payload, timeout=15)

    if response.status_code != 200:
        raise httpx.HTTPStatusError(message=response.text, request=response.request, response=response)

    return response.json()