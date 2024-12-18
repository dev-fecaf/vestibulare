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

    response = httpx.get(url=url, headers=headers, timeout=15)

    if response.status_code != 200:
        raise httpx.HTTPStatusError(message=response.text, request=response.request, response=response)

    return response.text # token


def executa_servico(servico: str, payload: dict):
    url = f'{base_url}/rest/servicoexterno/execute/{servico}'

    headers = {
        'token': gera_token(servico)
    }

    response = httpx.post(url=url, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise httpx.HTTPStatusError(message=response.text, request=response.request, response=response)

    return response.json()
