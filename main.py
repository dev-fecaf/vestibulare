from set_logger import logger
import settings as s
from datetime import date
import database as db
import api_vestibulare as api
import mentor_service as mentor
import httpx


COD_ERRO_ICA = 'ICA_00800'
TIPO_MEDIA = 'MFB'

# Variaveis de TESTE
ID_TURMA = '30'
ID_DISCIPLINA = '112'
DISCIPLINA = 'Língua Portuguesa'
# DISCIPLINA = 'Análise Linguística' # anglo
RGA = {'ra': '258'}
MENTOR_TURMA = s.MENTOR_TURMA
MENTOR_RA = s.MENTOR_RA
FALTAS = 1


def processar_turmas(periodo):
    turmas = api.turmas().get('turmas', {})
    turmas = {ID_TURMA: turmas[ID_TURMA]} if s.TEST else turmas

    for id_turma, turma_info in turmas.items():
        try:
            if ('infantil' or 'contraturno') in turma_info.get('nomeCompleto', '').lower():
                continue

            turma = db.records('query5.sql', params=(ANO_ATUAL, id_turma))
            if not turma and not s.TEST:
                logger.error(
                    f"Turma ID {turma_info['id']} nome {turma_info['nomeCompleto']} "
                    f"na vestibulare, não mapeada no mentor"
                )
                continue

            turma = MENTOR_TURMA if s.TEST else turma[0]['turma']
            alunos = buscar_alunos(turma)
            alunos = [RGA] if s.TEST else alunos
            if not alunos:
                logger.error(f'Nenhum aluno ativo retornado do mentor para a turma {turma}')
                continue

            processar_alunos(alunos, id_turma, turma_info, turma, periodo)
            print('Finalizado')
        except Exception:
            logger.exception('Erro ao processar turma')


def buscar_alunos(turma):
    alunos = db.records('query1.sql', params=(ANO_ATUAL, turma))
    if not alunos:
        logger.error(f'{turma} não encontrada no período {ANO_ATUAL} no mentor')
    return alunos


def processar_alunos(alunos, id_turma, turma_info, cod_turma, periodo):
    for aluno in alunos:
        rga = aluno['ra']
        try:
            medias = api.medias(
                rota='mediasBimestrais',
                acao='medias',
                rga=rga,
                id_turma=id_turma,
                periodo=periodo,
                ano=ANO_ATUAL
            )

            media_disciplinas = medias.get('resposta', {}).get('mediaPorDisciplina', {})

            medias_finais_resposta = api.medias(
                rota='mediasFinais',
                acao='mediasFinais',
                rga=rga,
                id_turma=id_turma,
                periodo=periodo,
                ano=ANO_ATUAL
            )
            medias_finais = medias_finais_resposta.get('resposta', {}).get('mediasFinais', {})

            processar_disciplinas(media_disciplinas, turma_info, rga, cod_turma, medias_finais)
        except httpx.HTTPStatusError:
            logger.exception(f'Erro ao processar aluno com RGA {rga}, possivel erro de turma diferente')
        except Exception:
            logger.exception(f'Erro ao processar aluno com RGA {rga}')


def processar_disciplinas(media_disciplinas, turma_info, rga, cod_turma, medias_finais):
    media_disciplinas = {ID_DISCIPLINA: media_disciplinas[ID_DISCIPLINA]} if s.TEST else media_disciplinas

    disciplinas = db.records('query6.sql', params=(ANO_ATUAL, cod_turma))

    for id_disciplina, disciplina_info in media_disciplinas.items():
        try:
            disciplina = next((item for item in disciplinas if int(item['id']) == int(id_disciplina)), {})
            disciplina = DISCIPLINA if s.TEST else disciplina.get('disciplina')

            if not disciplina:
                logger.error(
                    f"Disciplina {disciplina_info['disciplina']} da "
                    f"turma ID {turma_info['id']} nome {turma_info['nomeCompleto']} "
                    f"na vestibulare, não mapeada no mentor"
                )
                continue

            avaliacao = buscar_avaliacao(disciplina, rga, cod_turma, BIMESTRE)
            if not avaliacao:
                continue

            nota = disciplina_info.get('media')
            faltas = int(disciplina_info.get('faltas', 0))
            registrar_avaliacao(
                avaliacao=avaliacao,
                nota=nota,
                turma_info=turma_info,
                rga=rga,
                cod_turma=cod_turma,
                faltas=faltas
            )

            avaliacao_final = buscar_avaliacao(disciplina, rga, cod_turma, TIPO_MEDIA)
            if not avaliacao_final:
                continue
            media_final = medias_finais.get(id_disciplina, {}).get('media', 0)
            registrar_avaliacao(
                avaliacao=avaliacao_final,
                nota=media_final,
                turma_info=turma_info,
                rga=rga,
                cod_turma=cod_turma
            )
        except Exception:
            logger.exception('Erro ao processar disciplina')


def buscar_avaliacao(disciplina, rga, cod_turma, tipo_nota):
    rga = MENTOR_RA if s.TEST else rga

    params = (ANO_ATUAL, cod_turma, rga, disciplina, tipo_nota)
    avaliacao = db.records(sql_file='query2.sql', params=params)

    if avaliacao:
        avaliacao = avaliacao[0]
        if avaliacao.get('manual') == 1:
            logger.error(
                f'Nota da avaliação com os parametros: {params} tem alteração manual ativada.'
            )
    else:
        logger.error(f'Nenhuma avaliação encontrada para os parâmetros: {params}')

    return avaliacao


def registrar_avaliacao(avaliacao, nota, turma_info, rga, cod_turma, faltas=0):
    if nota:
        insere_falta(faltas, avaliacao, BIMESTRE, cod_turma)

        if str(nota) == avaliacao.get('nota_atual'):
            return

        nota_payload = {
            'idAvaliacao': avaliacao['apc_id'],
            'listAlunoNota': [{'idAluno': avaliacao['pes_id'], 'nota': nota}]
        }
        resultado = mentor.executa_servico(
            servico='gravaNotaAvaliacao', payload=nota_payload).get('valor')

        verificar_retorno_integracao(resultado, nota_payload, turma_info, rga)


def insere_falta(faltas, avaliacao, bimestre, cod_turma):
    if str(faltas) == str(avaliacao.get('faltas')):
        return

    faltas = FALTAS if s.TEST else faltas
    if faltas > 0:
        db.insert_or_update(
            sql_file='query4.sql',
            params=(
                faltas,
                avaliacao['id_ingresso'],
                avaliacao['id_disciplina'],
                bimestre,
                cod_turma
            )
        )


def verificar_retorno_integracao(resultado, nota_payload, turma_info, rga):
    if resultado.get('codigoRetornoIntegracao') == COD_ERRO_ICA:
        for aluno_nota in resultado.get('listAlunoNota', []):
            if aluno_nota['codigoRetornoIntegracao'] == COD_ERRO_ICA:
                logger.error(
                    f"{aluno_nota['observacaoRetornoIntegracao']} | "
                    f"nota: {aluno_nota['nota']} | id_avaliacao: {nota_payload['idAvaliacao']} | "
                    f"id_aluno: {nota_payload['listAlunoNota'][0]['idAluno']} | "
                    f"turma: {turma_info['id']} | RGA: {rga}"
                )


def processar_infantil(alunos, id_turma, turma_info, periodo):
    for aluno in alunos:
        rga = aluno['ra']
        try:
            medias = api.medias(
                rota='mediasBimestrais',
                acao='medias',
                rga=rga,
                id_turma=id_turma,
                periodo=periodo,
                ano=ANO_ATUAL
            )
            total_faltas = medias.get('resposta', {}).get('totalFaltas', {})



        except httpx.HTTPStatusError:
            logger.error(f'Aluno com RGA {rga} não encontrado na turma ID {turma_info['id']} '
                         f'nome {turma_info['nomeCompleto']} da vestibulare')
        except Exception:
            logger.exception(f'Erro ao processar aluno com RGA {rga}')


if __name__ == '__main__':
    try:
        ANO_ATUAL = date.today().year
        ANO_ATUAL = 2024
        for periodo in s.PERIODOS:
            periodo = int(periodo)
            BIMESTRE = f'M{periodo}'
            processar_turmas(periodo)
    except:
        logger.exception("Erro no processamento geral")
