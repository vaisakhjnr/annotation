import psycopg2
from config import config


def adminDeletePrice(requestParameters):
    conn = None
    price_value_id = requestParameters['price_value_id']
    status = requestParameters['status']
    price_value = requestParameters['price_value']

    #params = config()
    #conn = psycopg2.connect(**params)
    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")
    cur = conn.cursor()

    cur.execute("""UPDATE  price SET status = %(status)s , price_value = %(price_value)s 
                WHERE price_value_id=%(price_value_id)s;""",
                {"status": status, "price_value": price_value, "price_value_id": price_value_id}
                )
    cur.close()
    conn.commit()

    return {"message": "success"}
