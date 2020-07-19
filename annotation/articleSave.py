import psycopg2
from config import config


def articleSave(requestParameters):
    user_id = requestParameters['user_id']
    article_id = requestParameters['article_id']
    region_id = requestParameters['region_id']
    commodity_id = requestParameters['commodity_id']
    comm_desc_id = requestParameters['comm_desc_id']
    factor_id = requestParameters['factor_id']
    subfactor_id = requestParameters['subfactor_id']
    subfactorvalue_id = requestParameters['subfactorvalue_id']
    price_value_id = requestParameters['price_value_id']
    supply_value_id = requestParameters['supply_value_id']
    demand_value_id = requestParameters['demand_value_id']
    impact_region_id = requestParameters['impact_region_id']
    event_region_id = requestParameters['event_region_id']

    owner = requestParameters['owner']
    release_date = requestParameters['release_date']
    source = requestParameters['source']
    url = requestParameters['url']
    headline = requestParameters['headline']
    content = requestParameters['content']
    question = requestParameters['question']
    status = 'marked'

    isAnyMappingIdZero = False

    if user_id == 0 or article_id == 0 or region_id == 0 or commodity_id == 0 or comm_desc_id == 0 or factor_id == 0 or subfactor_id == 0 or subfactorvalue_id == 0 or price_value_id == 0 or supply_value_id == 0 or demand_value_id == 0 or impact_region_id == 0 or event_region_id == 0:
        isAnyMappingIdZero = True

    if question == 'NULL':
        status = 'completed'
        question = ''

    # params = config()
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect(host="localhost", database="annotation", user="postgres", password="pass")
    cur = conn.cursor()

    cur.execute("""UPDATE master_table SET release_date = %(release_date)s , source = %(source)s , headline = %(headline)s, content = %(content)s , question = %(question)s,  status = %(status)s 
    WHERE article_id = %(article_id)s;""",
                {'owner': owner, 'release_date': release_date, 'source': source, 'url': url, 'headline': headline,
                 'content': content, 'question': question, 'status': status, 'article_id': article_id}
                )
    cur.close()
    conn.commit()

    cur = conn.cursor()
    cur.execute("""SELECT EXISTS (SELECT 1 FROM mapping_table
     WHERE article_id = %(article_id)s AND region_id = %(region_id)s AND commodity_id = %(commodity_id)s AND comm_desc_id = %(comm_desc_id)s AND factor_id = %(factor_id)s AND subfactor_id = %(subfactor_id)s AND subfactorvalue_id = %(subfactorvalue_id)s AND price_value_id = %(price_value_id)s AND supply_value_id = %(supply_value_id)s AND demand_value_id = %(demand_value_id)s AND impact_region_id = %(impact_region_id)s AND event_region_id = %(event_region_id)s LIMIT 1);""",
                {'article_id': article_id, 'region_id': region_id, 'commodity_id': commodity_id,
                 'comm_desc_id': comm_desc_id, 'factor_id': factor_id, 'subfactor_id': subfactor_id,
                 'subfactorvalue_id': subfactorvalue_id, 'price_value_id': price_value_id,
                 'supply_value_id': supply_value_id, 'demand_value_id': demand_value_id,
                 'impact_region_id': impact_region_id, 'event_region_id': event_region_id})

    mappingExist = cur.fetchone()
    mappingExist = mappingExist[0]

    if not mappingExist and not isAnyMappingIdZero:
        cur.execute("""INSERT INTO mapping_table (user_id, article_id, region_id, commodity_id, comm_desc_id, factor_id, subfactor_id, subfactorvalue_id, price_value_id, supply_value_id, demand_value_id, impact_region_id, event_region_id, status)
        VALUES (%(user_id)s, %(article_id)s, %(region_id)s, %(commodity_id)s, %(comm_desc_id)s, %(factor_id)s, %(subfactor_id)s, %(subfactorvalue_id)s, %(price_value_id)s, %(supply_value_id)s, %(demand_value_id)s, %(impact_region_id)s, %(event_region_id)s, 'enabled');""",
                    {'user_id': user_id, 'article_id': article_id, 'region_id': region_id,
                     'commodity_id': commodity_id,
                     'comm_desc_id': comm_desc_id, 'factor_id': factor_id, 'subfactor_id': subfactor_id,
                     'subfactorvalue_id': subfactorvalue_id, 'price_value_id': price_value_id,
                     'supply_value_id': supply_value_id,
                     'demand_value_id': demand_value_id, 'impact_region_id': impact_region_id,
                     'event_region_id': event_region_id})

    else:
        return "success article only"

    cur.close()
    conn.commit()
    conn.close()
    if isAnyMappingIdZero: return "success article only"
    return "success"
