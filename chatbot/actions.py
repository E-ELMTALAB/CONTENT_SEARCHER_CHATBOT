import traceback
import psycopg2
import psycopg2.extras

class Actions():
    def __init__(self):
        self.hostname = 'localhost'
        self.database = 'content_label'
        self.username = 'postgres'
        self.pwd = 'arshanelmtalab1398a'
        self.port_id = 5432
        self.image_csv_path = r"data/csv/image_info.csv"


    def db_connection(func):
        @wraps(func)
        def wrapper(self , *args, **kwargs):
            conn = None
            cur = None

            try:
                conn = psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pwd,
                    port=self.port_id
                )
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                # Call the original function with the connection and cursor as additional arguments
                result = func(self, conn, cur, *args, **kwargs)

                return result

            except Exception as error:
                traceback.print_exc()
                return None

            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

        return wrapper


    def find_request(self , objects):
        # attributes for connecting to the database
        hostname = 'localhost'
        database = 'content_label'
        username = 'postgres'
        pwd = 'arshanelmtalab1398a'
        port_id = 5432
        conn = None

        # connecting to the database
        try:
            with psycopg2.connect(
                    host=hostname,
                    dbname=database,
                    user=username,
                    password=pwd,
                    port=port_id) as conn:

                with conn.cursor(
                        cursor_factory=psycopg2.extras.DictCursor) as cur:  # for writing or reading from database

                    # # inseting value script
                    # insert_script = 'INSERT INTO public.recommend_song(userid , songid) VALUES (%s , %s)'
                    #
                    # # inserting each recommendation song of each user id to the recommend_song table
                    # for recom in recom_list:
                    #     cur.execute(insert_script, (user_id, recom))
                    #     conn.commit()

                    cur.execute('SELECT * FROM public.images')
                    print(cur.fetchall())

        except Exception as error:
            traceback.print_exc()
        finally:  # close the connection to the database
            if conn is not None:
                conn.close()


if __name__ == "__main__":
    action = Actions()
    action.find_request()