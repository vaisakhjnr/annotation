import psycopg2
from config import config


def adminUsersFetch(requestParameters):
    # params = config()
    # conn = psycopg2.connect(**params)

    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")
    cur = conn.cursor()
    page = requestParameters['page']
    offset = (page-1)*20
    limit = 20

    cur.execute("""SELECT COUNT(user_id) FROM users;""")
    dataCount = cur.fetchall()
    dataCount = dataCount[0]
    pageCount = dataCount[0]//20
    if (dataCount[0] % 20) != 0 and dataCount[0] > 20:
        pageCount = pageCount + 1
        
    cur.execute("""SELECT user_id, username, email, phone, pass_key, status, privilege FROM users WHERE status = 'enabled' LIMIT %(limit)s OFFSET %(offset)s;""", {"limit": limit, "offset": offset})
    valueList = []
    rows = cur.fetchall()
    for row in rows:
        value = {"user_id": row[0], "username": row[1], "email": row[2], 'phone': row[3], 'pass_key': row[4],
                 'status': row[5], 'privilege': row[6]}
        valueList.append(value)
    cur.close()
    conn.commit
    conn.close()
    return {'data': valueList, 'pages': pageCount}
    