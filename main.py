from set_logger import logger, nota
from database import records
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
                alunos = records('query1.sql', params=(ano_atual, turma))
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
                        avaliacao = records(sql_file='query2.sql', params=params)
                        if not avaliacao:
                            logger.error(f'Nenhuma avaliação encontrada para os parametros: {params}')
                            continue

                        avaliacao = avaliacao[0]
                        media = media_disciplinas.get(id_disciplina)
                        if media:
                            nota = media['media']
                            resultado = mentor.grava_nota(
                                id_avaliacao=avaliacao['apc_id'], id_aluno=avaliacao['pes_id'], nota=nota
                            )
                            print(resultado)
                        else:
                            logger.error(f'Disciplina {disciplina} ID {id_disciplina} sem nota lançada')
                            continue
                    else:
                        logger.error(f'Diciplina ID {id_disciplina} não mapeada')
                except:
                    logger.exception('Disciplina')
                    continue

except Exception as e:
    logger.exception(e)
