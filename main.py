from set_logger import logger
import database as db
from dict_turmas import turmas
from dict_disciplinas import disciplinas
from datetime import date
import api
import mentor

ano_atual = date.today().year

periodo = 1
bimestre = f'{periodo}º Bimestre'
alunos = []
turma = ''

try:
    turmas_vestibulare = api.turmas()['turmas']

    for id_turma in turmas_vestibulare:
        try:
            if turmas.get(id_turma):
                turma = turmas[id_turma]
                alunos = db.records('query1.sql', params=(ano_atual, turma))
                if not alunos:
                    logger.error(f'{turma} não encontrada no periodo {ano_atual}')
                    continue
            else:
                logger.error(f'Turma ID {id_turma} não mapeada')
        except:
            logger.exception('Turma')
            continue

        for aluno in alunos:
            try:
                rga = aluno['ra']
                media_disciplinas = api.medias_bimestrais(
                    rga=rga, id_turma=id_turma, periodo=periodo, ano=ano_atual
                )['resposta']['mediaPorDisciplina']
            except:
                logger.exception('Aluno')
                continue

            for id_disciplina in media_disciplinas:
                try:
                    if disciplinas.get(id_disciplina):
                        disciplina = disciplinas[id_disciplina]
                        params = (ano_atual, turma, rga, disciplina, bimestre)
                        avaliacao = db.records(sql_file='query2.sql', params=params)
                        if not avaliacao:
                            logger.error(f'Nenhuma avaliação encontrada para os parametros: {params}')
                            continue

                        avaliacao = avaliacao[0]
                        media = media_disciplinas.get(id_disciplina)
                        if media:
                            nota = media['media']
                            pes_id = avaliacao['pes_id']
                            apc_id = avaliacao['apc_id']
                            id_ingresso = avaliacao['id_ingresso']
                            id_discip = avaliacao['id_disciplina']

                            list_aluno_nota = [{
                                'idAluno': pes_id,
                                'nota': nota
                            }]

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
                                            f"nota: {aluno_nota['nota']} | id_avaliacao: {apc_id} | "
                                            f"id_aluno: {pes_id} | parametros: {params}"
                                        )

                            faltas = media['faltas']
                            if faltas > 0:
                                params = (faltas, id_ingresso, id_discip)
                                db.insert(sql_file='query4.sql', params=params)
                    else:
                        logger.error(f'Diciplina ID {id_disciplina} não mapeada')
                except:
                    logger.exception('Disciplina')
                    continue

except Exception as e:
    logger.exception(e)
