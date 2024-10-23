faltas = media['faltas']
if faltas > 0:
    params = (faltas, turma, disciplina, ano_atual)
    cronograma = records(sql_file='query3.sql', params=params)

    if len(cronograma) < faltas:
        logger.exception(
            f'Quantidade de aulas menor do que a quantidade de faltas | '
            f'quantidade de aulas no cronograma: {len(cronograma)} | '
            f'quantidade de faltas: {faltas} | aluno_ra: {rga} | parametros: {params}'
        )

    insere_faltas = []
    atualiza_cronograma = []
    atualiza_historico = []

    for data_aula in cronograma:
        data_falta = data_aula['cad_data'].strftime('%d/%m/%Y')

        insere_faltas.append({
            'Cod_turma': turma,
            'Cod_discip': data_aula['cod_disciplina'],
            'Cod_aluno': rga,
            'Data_falta': data_falta
        })
        atualiza_cronograma.append({
            'Cod_turma': turma,
            'Cod_discip': data_aula['cod_disciplina'],
            'Data_falta': data_falta
        })
        atualiza_historico.append({
            'Cod_turma': turma,
            'Cod_discip': data_aula['cod_disciplina'],
            'Cod_aluno': rga
        })

    falta_payload = {
        'INSERE_FALTAS': insere_faltas,
        'ATUALIZA_CRONOGRAMA': atualiza_cronograma,
        'ATUALIZA_HISTORICO': atualiza_historico
    }

    result_falta = mentor.executa_servico(servico='insereFalta', payload=falta_payload)

    if result_falta['resultado'] == 'ERRO':
        logger.error(f'Inserção de faltas: {result_falta["erro"]} | params: {params}')