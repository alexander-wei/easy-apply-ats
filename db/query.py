"""
Created on Aug 8, 2024

@author: alexander
"""

from sqlalchemy import text

SELECT_QUERY = """
select url from
(
select max(date) date, url from 
(
select t.url, t.date from (SELECT p.*, a.app_id FROM jobapps.applications a right join jobapps.postings p on id=posting_id 
where
a.app_id is null

order by title asc   )   t 

where url not in 
(SELECT distinct(url) FROM jobapps.applications inner join jobapps.postings on id=posting_id )
) A
group by url
order by date desc
) B
;
"""


def rows_as_dicts(cursor):
    """convert tuple result to dict with cursor"""
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]


class DBQuery:

    @staticmethod
    def get_incomplete_urls(db):
        with db.engine.connect() as conn:
            result = conn.execute(text(SELECT_QUERY))
            # print(result.all())
            __ = rows_as_dicts(result.cursor)
        return [p["url"] for p in __]


if __name__ == "__main__":
    import db

    url_list = DBQuery.get_incomplete_urls(db)
    pass
