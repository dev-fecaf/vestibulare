SELECT TOP %s
CAD_ID as cad_id,
CAD_DATA as cad_data,
DIS_DISTEL as cod_disciplina
FROM TB_CRONOGRAMA_AULA
INNER JOIN TB_CRONOGRAMA_AULA_DATA on (CAU_CADID = CAD_ID)
INNER JOIN TB_TURMA_DISCIP ON (CAD_TDIID = TDI_TURDISID)
INNER JOIN TB_MESTRE_DISCIPLINA MDI ON (TDI_TURDISID = MDI_TURDISID)
INNER JOIN TB_MESTRE_ALUNO ON (MDI_MALID = MAL_ID)
INNER JOIN TB_INGRESSO ON (MAL_INGID = ING_ID)
INNER JOIN TB_PESSOA ALU ON (ING_PESID = PES_ID)
INNER JOIN TB_TURMA tt ON (TDI_TURID = TUR_ID)
INNER JOIN TB_PERIODO_LETIVO tpl ON (tpl.PEL_PERID = tt.TUR_PERID)
INNER JOIN TB_DISCIPLINA ON (TDI_DISCID = DIS_DISID)
INNER JOIN TB_HORARIO ON (CAU_HORID = HOR_ID)
WHERE TUR_CODTUR = %s
AND DIS_DESDIS = %s
AND tpl.PEL_ANOREF = %s
ORDER BY CAD_ID ASC
