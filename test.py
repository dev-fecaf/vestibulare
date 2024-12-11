from set_logger import logger
import database as db
from dict_turmas import turmas
from dict_disciplinas import disciplinas
import api_vestibulare
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
    avaliacao = db.records(sql_file='query2.sql', params=params)
    if not avaliacao:
        logger.error(f'Nenhuma avaliação encontrada para os parametros: {params}')

    avaliacao = avaliacao[0]
    media = media_disciplinas.get(id_disciplina)
    if media:
        nota = media['media']
        pes_id = avaliacao['pes_id']
        apc_id = avaliacao['apc_id']
        id_ingresso = avaliacao['id_ingresso']
        id_discip = avaliacao['id_disciplina']

        list_aluno_nota = [
            {
                'idAluno': pes_id,
                'nota': nota
            }
        ]

        nota_payload = {
            'idAvaliacao': apc_id,
            'listAlunoNota': list_aluno_nota
        }

        grava_nota = mentor.executa_servico(servico='gravaNotaAvaliacao', payload=nota_payload)

        resultado = grava_nota['valor']
        cod_erro = 'ICA_00800'
        if resultado['codigoRetornoIntegracao'] == cod_erro:
            for aluno_nota in resultado['listAlunoNota']:
                if aluno_nota['codigoRetornoIntegracao'] == cod_erro:
                    logger.error(
                        f"{aluno_nota['observacaoRetornoIntegracao']} | "
                        f"nota: {aluno_nota['nota']} | id_avaliacao: {apc_id} | id_aluno: {pes_id} | "
                        f"parametros: {params}"
                    )

        faltas = media['faltas']
        if faltas > 0:
            params = (faltas, id_ingresso, id_discip)
            db.insert(sql_file='query4.sql', params=params)

    print('FINALIZADO')

except:
    logger.exception('TEST')
