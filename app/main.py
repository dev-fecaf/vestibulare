import processo as pr
from datetime import date
import settings as s

ANO_ATUAL = date.today().year
ANO_ATUAL = 2024 # remover depois

for periodo in tuple(s.PERIODOS):
    periodo = int(periodo)
    BIMESTRE = f'M{periodo}'
    pr.processar_turmas(periodo, ANO_ATUAL, BIMESTRE)
