from set_logger import logger

from pymssql import connect, Error
import settings as s

conn_params = {
    'host': s.MS_HOST,
    'port': s.MS_PORT,
    'user': s.MS_USER,
    'password': s.MS_PASSWORD,
    'database': s.MS_DB
}

def records(sql_file: str, params: tuple = None):
    try:
        with connect(**conn_params) as conn:
            with conn.cursor(as_dict=True) as cur:
                with open(f'queries/{sql_file}') as f:
                    cur.execute(f.read(), params)
                return cur.fetchall()
    except Error:
        logger.exception('SQLServer records')


def insert_or_update(sql_file: str, params: tuple = None):
    try:
        with connect(**conn_params) as conn:
            with conn.cursor() as cur:
                with open(f'queries/{sql_file}') as f:
                    cur.execute(f.read(), params)
            conn.commit()
    except Error:
        logger.exception('SQLServer insert_or_update')


def atualiza_tag(ra, tag):
    sql = f"""
    UPDATE TB_PESSOA
    SET PES_INTEG_OUTROS = 
        CASE
            WHEN PES_INTEG_OUTROS IS NULL THEN ''
            WHEN PES_INTEG_OUTROS NOT LIKE '%{tag}%' THEN PES_INTEG_OUTROS + '{tag}/'
            ELSE PES_INTEG_OUTROS
        END
    WHERE PES_CODTEL = '{ra}';        
    """
    try:
        with connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
    except Error:
        logger.exception('SQLServer atualiza_tag')


if __name__ == '__main__':
    with connect(**conn_params) as conn:
        with conn.cursor(as_dict=True) as cur:
            cur.execute('SELECT TOP 1 * FROM TB_PESSOA')
            print(cur.fetchall())
