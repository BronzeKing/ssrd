# encoding: utf-8

from django.db import connections


def run_query_sql(strSql, args=None):
    """
            直接运行sql语句
    """

    connection = connections['default']
    cursor = connection.cursor()
    result_rows = []
    try:
        if args:
            cursor.execute(strSql, args)
        else:
            cursor.execute(strSql)
    finally:
        cursor.close()
        connection.close()
    return result_rows

def source():
    run_query_sql('source ssrd.sql')
    #  with open('ssrd.sql', 'r') as fd:
        #  for line in fd.readlines():
            #  sql = line.strip('\n')
            #  run_query_sql(sql)
