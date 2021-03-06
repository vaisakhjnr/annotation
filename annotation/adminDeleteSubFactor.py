import psycopg2
from config import config


def adminDeleteSubFactor(requestParameters):
    subfactor_id = requestParameters['subfactor_id']
    status = requestParameters['status']
    subfactor = requestParameters['subfactor']
    factor_id = requestParameters['factor_id']

    # params = config()
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")
    cur = conn.cursor()

    cur.execute("""UPDATE  subfactor_table SET status = %(status)s , subfactor = %(subfactor)s , factor_id = %(factor_id)s
                WHERE subfactor_id=%(subfactor_id)s;""",
                {"status": status, "subfactor": subfactor, "subfactor_id": subfactor_id, "factor_id": factor_id})

    cur.execute("""UPDATE  subfactorvalue_table SET status = %(status)s, subfactor_id =%(subfactor_id)s ,factor_id = %(factor_id)s
     WHERE subfactor_id=%(subfactor_id)s;""",
                {"status": status, "subfactor_id": subfactor_id, "factor_id": factor_id})

    cur.close()
    conn.commit()

    return {"message": "success"}
