import json

from set_logger import logger
from database import records
from dict_turmas import turmas
from dict_disciplinas import disciplinas
import api
import mentor


ano_atual = 2024
periodo = 1
bimestre = f'{periodo}º Bimestre'
id_turma = '30'
id_disciplina = '112'
rga = '258'

turma = turmas[id_turma]

try:
    media_disciplinas = api.medias_bimestrais(
        rga=rga, id_turma=int(id_turma), periodo=periodo, ano=ano_atual
    )['resposta']['mediaPorDisciplina']

    disciplina = disciplinas[id_disciplina]
    params = (ano_atual, turma, rga, disciplina, bimestre)
    avaliacao = records(sql_file='query2.sql', params=params)
    if not avaliacao:
        logger.error(f'Nenhuma avaliação encontrada para os parametros: {params}')

    avaliacao = avaliacao[0]
    media = media_disciplinas.get(id_disciplina)
    if media:
        nota = media['media']
        pes_id = avaliacao['pes_id']
        apc_id = avaliacao['apc_id']
        grava_nota = mentor.grava_nota(
            id_avaliacao=apc_id, id_aluno=pes_id, nota=nota
        )

        resultado = grava_nota['valor']
        if resultado['codigoRetornoIntegracao'] == 'ICA_00800':
            for aluno_nota in resultado['listAlunoNota']:
                if aluno_nota['codigoRetornoIntegracao'] == 'ICA_00800':
                    logger.error(
                        f"{aluno_nota['observacaoRetornoIntegracao']} | "
                        f"nota: {aluno_nota['nota']} | id_avaliacao: {apc_id} | id_aluno: {pes_id} | "
                        f"parametros: {params}"
                    )


    else:
        print(f'Disciplina ID {id_disciplina} sem nota lançada')

except:
    logger.exception('TEST')
