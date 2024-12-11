SELECT
    td.DIS_OBSERV as id,
    td.DIS_DESDIS as disciplina
FROM
	TB_TURMA tt
	INNER JOIN TB_PERIODO_LETIVO tpl ON tt.TUR_PERID = tpl.PEL_PERID
	INNER JOIN TB_TURMA_DISCIP ttd ON tt.TUR_ID = ttd.TDI_TURID
	INNER JOIN TB_DISCIPLINA td ON td.DIS_DISID = ttd.TDI_DISCID
WHERE
	tpl.PEL_ANOREF = %s AND
	tt.TUR_CODTUR = %s