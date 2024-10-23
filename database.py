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
        logger.exception('SQLServer')
        exit('Erro no banco SQLServer')


def insert(sql_file: str, params: tuple = None):
    with connect(**conn_params) as conn:
        with conn.cursor() as cur:
            with open(f'queries/{sql_file}') as f:
                cur.execute(f.read(), params)
        conn.commit()


if __name__ == '__main__':
    from dict_turmas import turmas
    r = records('query1.sql', params=(2024, turmas['30']))
    print(r)
