import psycopg2
from config import config


def markIrrelevant(requestParameters):
    article_id = requestParameters["article_id"]

    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute("""UPDATE master_table set status = 'irrelevant'
        where article_id = %(article_id)s;""", {"article_id": article_id})
    cur.close()
    conn.commit()
    conn.close()
    return
