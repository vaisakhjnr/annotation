import psycopg2
from config import config


def articleContentNav(requestParameters):
    conn = None
    article_id = requestParameters['article_id']
    user_id = requestParameters['user_id']
    direction = requestParameters['flag']
    last_article = requestParameters['last_article']

    # params = config()
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")
    cur = conn.cursor()

    cur.execute("SELECT privilege FROM users WHERE user_id = %(user_id)s; ",
                {'user_id': user_id})
    privilege = cur.fetchone()
    privilege = privilege[0]

    if privilege == '1':
        if direction == 0:
            cur.execute("""SELECT COUNT(article_id)
                FROM master_table
                WHERE article_id <= %(article_id)s;""", {"article_id": article_id, "user_id": user_id})
            todoCount = cur.fetchone()
            todoCount = todoCount[0]

        else:
            cur.execute("""SELECT COUNT(article_id)
                FROM master_table
                WHERE article_id >= %(article_id)s;""", {"article_id": article_id, "user_id": user_id})
            todoCount = cur.fetchone()
            todoCount = todoCount[0]

    else:
        if direction == 0:
            cur.execute("""SELECT COUNT(article_id)
                FROM master_table
                WHERE article_id <= %(article_id)s AND user_id= %(user_id)s;""",
                        {"article_id": article_id, "user_id": user_id})
            todoCount = cur.fetchone()
            todoCount = todoCount[0]

        else:
            cur.execute("""SELECT COUNT(article_id)
                FROM master_table
                WHERE article_id >= %(article_id)s AND user_id= %(user_id)s;""",
                        {"article_id": article_id, "user_id": user_id})
            todoCount = cur.fetchone()
            todoCount = todoCount[0]

    if todoCount == 0:
        return {"message": "empty"}
    
    if last_article == 'yes':
        cur.execute("""SELECT last_open_article_id FROM users WHERE user_id = %(user_id)s LIMIT 1""", {"article_id": article_id, "user_id": user_id})
        article_id = cur.fetchone()
        article_id = article_id[0]

    if last_article != 'yes':
        cur.execute("""SELECT owner, release_date, source, url, headline, content, question, last_modified_date,last_modified_by, article_id, status
            FROM master_table 
            WHERE article_id = %(article_id)s LIMIT 1;""",
                    {"article_id": article_id}
                    )
    else:
        if privilege == '1':
            if direction == 0:
                cur.execute("""SELECT owner, release_date, source, url, headline, content, question, last_modified_date,last_modified_by, article_id, status
                    FROM master_table 
                    WHERE article_id <= %(article_id)s ORDER BY article_id DESC LIMIT 1;""",
                            {"article_id": article_id}
                            )
            elif direction == 1:
                cur.execute("""SELECT owner, release_date, source, url, headline, content, question, last_modified_date,last_modified_by, article_id, status
                    FROM master_table 
                    WHERE article_id >= %(article_id)s ORDER BY article_id ASC LIMIT 1;""",
                            {"article_id": article_id}
                            )
            else:
                cur.execute("""SELECT owner, release_date, source, url, headline, content, question, last_modified_date,last_modified_by, article_id, status
                    FROM master_table 
                    WHERE article_id = %(article_id)s ORDER BY article_id ASC LIMIT 1;""",
                            {"article_id": article_id}
                            )
        else:
            if direction == 0:
                cur.execute("""SELECT owner, release_date, source, url, headline, content, question, last_modified_date,last_modified_by, article_id, status
                    FROM master_table 
                    WHERE article_id <= %(article_id)s AND user_id= %(user_id)s ORDER BY article_id DESC LIMIT 1;""",
                            {"article_id": article_id, "user_id": user_id}
                            )
            elif direction == 1:
                cur.execute("""SELECT owner, release_date, source, url, headline, content, question, last_modified_date,last_modified_by, article_id, status
                    FROM master_table 
                    WHERE article_id >= %(article_id)s AND user_id= %(user_id)s ORDER BY article_id ASC LIMIT 1;""",
                            {"article_id": article_id, "user_id": user_id}
                            )
            else:
                cur.execute("""SELECT owner, release_date, source, url, headline, content, question, last_modified_date,last_modified_by, article_id, status
                    FROM master_table 
                    WHERE article_id = %(article_id)s ORDER BY article_id ASC LIMIT 1;""",
                            {"article_id": article_id}
                            )
        

    row = cur.fetchall()
    owner = row[0][0]
    release_date = row[0][1]
    source = row[0][2]
    url = row[0][3]
    headline = row[0][4]
    content = row[0][5]
    question = row[0][6]
    last_modified_date = row[0][7]
    last_modified_by = row[0][8]
    article_id = row[0][9]
    status = row[0][10]

    #cur.execute(
    #    """SELECT username FROM users WHERE user_id = %(user_id)s LIMIT 1;""",
    #    {"user_id": owner}
    #)
    #row = cur.fetchall()
    #ownername = row[0][0]

    returnList = {'owner': owner, 'release_date': release_date, 'source': source, 'url': url, 'headline': headline,
                  'content': content, 'question': question, 'last_modified_date': last_modified_date,
                  'last_modified_by': last_modified_by, 'article_id': article_id, 'status': status, 'count': todoCount}

    cur.execute("""UPDATE users SET last_open_article_id = %(article_id)s where user_id = %(user_id)s""", {"article_id": article_id, "user_id": user_id})

    cur.close()
    conn.commit()
    return returnList
