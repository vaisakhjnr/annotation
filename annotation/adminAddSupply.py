import psycopg2
from config import config


def adminAddSupply(requestParameters):
    conn = None
    supply_value = requestParameters['supply_value']

    #params = config()
    #conn = psycopg2.connect(**params)
    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO supply (supply_value,status) VALUES (%(supply_value)s,'enabled');", {'supply_value': supply_value})
    conn.commit()

    cur.execute("SELECT EXISTS (SELECT 1 FROM supply WHERE supply_value = %(supply_value)s LIMIT 1);",
                {'supply_value': supply_value})
    userExists = cur.fetchone()
    userExists = userExists[0]

    if userExists:
        cur.execute("SELECT supply_value_id FROM supply WHERE supply_value = %(supply_value)s;",
                    {'supply_value': supply_value})
        supply_value_id = cur.fetchone()
        supply_value_id = supply_value_id[0]
        return {'supply_value_id': supply_value_id}
    else:
        return "failed"
