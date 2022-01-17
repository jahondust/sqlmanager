from apps.queries.connections.ssh import open_ssh_tunnel
import psycopg2
from psycopg2 import Error


class Connect:
    query = None
    database = None

    def __init__(self, query):
        self.query = query
        self.database = query.database

    def run(self, request):
        tunnel = None
        connection = None
        cursor = None
        result = {}

        host = self.database.host
        port = self.database.port
        if self.database.use_ssh:
            tunnel = open_ssh_tunnel(self.database)
            port = tunnel.local_bind_port
            host = '127.0.0.1'
        try:
            connection = psycopg2.connect(user=self.database.user_name,
                                          password=self.database.password,
                                          host=host,
                                          port=port,
                                          database=self.database.db_name)

            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            #Ordering
            order_by = request.GET.get('ordering', self.query.order_by)
            order_sql = """ORDER BY """
            if order_by[:1] == '-':
                order_sql += f"""{order_by[1:]} DESC"""
            else:
                order_sql += f"""{order_by}"""

            #Pagination
            page = None
            if self.query.pagination:
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', self.query.page_size))
                offset = (page-1) * page_size
                pagination_sql = f"""LIMIT {page_size} OFFSET {offset}"""
            else:
                pagination_sql = ""

            #Filter
            params = {}
            for param in self.query.params.all():
                params[param.name] = request.GET.get(param.name, param.default)

            sql_query = f"""
                SELECT * FROM ({self.query.query}) AS tbl
                {order_sql}
                {pagination_sql}
            """
            cursor.execute(sql_query, params)
            data = cursor.fetchall()

            #Total count
            sql_query = f"""
                SELECT count(*) FROM ({self.query.query}) AS tbl
            """
            cursor.execute(sql_query, params)
            count = cursor.fetchone()
            result = {
                'count': count['count'],
                'page': page,
                'data': data
            }
        except (Exception, Error) as error:
            return {
                'error': "Error while connecting to PostgreSQL " + str(error)
            }
        finally:
            if connection:
                cursor.close()
                connection.close()

        if self.database.use_ssh:
            tunnel.close()

        return result
