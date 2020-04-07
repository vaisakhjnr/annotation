import psycopg2
from annotation.config import config


def fetchFactorValue(requestParameters):
    # params = config()
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")
    cur = conn.cursor()
    is_null = requestParameters['is_null']
    page = requestParameters['page']
    offset = (page-1)*10
    limit = offset + 10

    cur.execute("""SELECT COUNT(factor_value_id) FROM factor_value_table;""")
    dataCount = cur.fetchall()
    dataCount = dataCount[0]
    pageCount = dataCount[0]//10
    if (dataCount[0] % 10) != 0:
        pageCount = pageCount + 1

    if is_null == 'NULL':
        cur.execute("SELECT EXISTS (SELECT 1 FROM factor_value_table LIMIT 1);")

        valueExists = cur.fetchone()
        valueExists = valueExists[0]

        if not valueExists:
            return {'message': "no values"}

        cur.execute("""SELECT factor_value, factor_value_id, status
            FROM factor_value_table LIMIT %(limit)s OFFSET %(offset)s;""", {"limit": limit, "offset": offset})
        rows = cur.fetchall()
        valueList = []
        for row in rows:
            value = {"factor_value": row[0], "factor_value_id": row[1], "status": row[2]}
            valueList.append(value)


        cur.close()
        conn.commit()

        return {'data': valueList, 'pages': pageCount}
        
    elif is_null == 'enabled':
        cur.execute("SELECT EXISTS (SELECT 1 FROM factor_value_table LIMIT 1);")

        valueExists = cur.fetchone()
        valueExists = valueExists[0]

        if not valueExists:
            return {'message': "no values"}

        cur.execute("""SELECT factor_value, factor_value_id, status
            FROM factor_value_table WHERE status='enabled';""")
        rows = cur.fetchall()
        valueList = []
        for row in rows:
            value = {"factor_value": row[0], "factor_value_id": row[1], "status": row[2]}
            valueList.append(value)


        cur.close()
        conn.commit()

        return {'data': valueList}

    factor_value_id = requestParameters["factor_value_id"]

    cur.execute("""SELECT factor_value
           FROM factor_value_table
           WHERE factor_value_id= %(factor_value_id)s ;""", {"factor_value_id": factor_value_id})
    row = cur.fetchone()
    factor_value = row[0]

    return factor_value
