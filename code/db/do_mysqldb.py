#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://www.python.org/dev/peps/pep-0249/
# https://mysqlclient.readthedocs.io/user_guide.html#

from MySQLdb import _mysql
import MySQLdb

cfg1 = {'host': '10.172.xxx.xxx', 'port': 3301, 'user': 'admin', 'passwd': 'admin@123456', 'db': 'test_db'}
cfg2 = {'host': '10.172.xxx.xxx', 'port': 3301, 'user': 'admin', 'password': 'admin@123456', 'database': 'test_db'}


def api__mysql(conn):
    """
    use_result() returns the entire result set to the client immediately, If your result set is really large  this
    could be a problem. One way around this is to add a LIMIT clause to your query, to limit the number of rows returned.
    """
    # rs = conn.store_result()

    """use_result(), which keeps the result set in the server and sends it row-by-row when you fetch. This does, 
    however, tie up server resources, and it ties up the connection: You cannot do any more queries until you have 
    fetched all the rows. Generally I recommend using store_result() unless your result set is really huge and you 
    can’t use LIMIT for some reason """
    conn.query("""select cid
                    ,cname        
            from courses""")
    rs = conn.use_result()
    print(type(rs))
    print(rs.fetch_row())
    print(rs.fetch_row())
    print(rs.fetch_row())

    conn.commit()


def api_mysqldb(conn):
    """
    MySQLdb is a thin Python wrapper around _mysql which makes it compatible with the Python DB API interface (
    version 2). In reality, a fair amount of the code which implements the API is in _mysql for the sake of
    efficiency. :param conn: :return:
    """
    cur = conn.cursor()
    cur.execute("""SELECT cid, cnum FROM cards
              WHERE cid > %s""", (2,))

    print(type(cur.fetchone()))

    rs = cur.fetchall()
    print(type(rs))

    print(cur.fetchone())

    cur.executemany(
        """INSERT INTO cards (cid, cnum)
        VALUES (%s, %s)""",
        [
            (6, "2021111004"),
            (7, "2021111005")
        ])

    conn.commit()

    cur.execute("""SELECT cid, cnum FROM cards
              WHERE cid > %s""", (2,))

    print(cur.fetchone())
    print(cur.fetchone())
    print(cur.fetchone())


if __name__ == "__main__":
    conn1 = _mysql.connect(**cfg1)
    api__mysql(conn1)
    print('\n-----------------------------\n')
    conn2 = MySQLdb.connect(**cfg2)
    api_mysqldb(conn2)
