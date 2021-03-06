import psycopg2
#from config import config


def testData():
    # params = config()
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")

    user_id = "999"
    
    cur = conn.cursor()

    headline = "Test Headline"
    content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sed feugiat risus. Nunc mauris nisi, gravida non nulla dapibus, laoreet pretium purus. Donec aliquam orci at ipsum congue, at bibendum metus lobortis."
    owner = 999
    release_date = "2020-04-24"
    source = "Test Source"
    url = "Test URL"
    question = ''
    status = 'todo'

    for i in range(50000):
        cur.execute("""INSERT INTO master_table (user_id, headline, content, owner, release_date, source, url, question, status) 
        VALUES ( %(user_id)s, %(headline)s, %(content)s, %(owner)s, %(release_date)s, %(source)s, %(url)s, %(question)s, %(status)s );""",
                    {'user_id': user_id, 'headline': headline, 'content': content, 'owner': owner,
                    'release_date': release_date, 'source': source, 'url': url, 'question': question,
                    'status': status})
    cur.close()
    conn.commit()

    conn.close()
    return {"message": "success"}
