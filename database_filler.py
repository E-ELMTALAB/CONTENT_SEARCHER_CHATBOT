import traceback
import psycopg2
import psycopg2.extras
import pandas as pd
from tqdm import tqdm
from functools import wraps

class Database_Filler():

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

    @db_connection
    def perform_database_operation(self, conn, cur):
        try:
            cur.execute('SELECT * FROM public.images')
            return cur.fetchall()

        except Exception as error:
            traceback.print_exc()
            return None

    def change_filepath(self , head_path):
        base_path = "data/"
        path = (base_path + head_path[8:]).replace("/" , "\\")
        return path


    # def push_image_info(self , csv_path):
    #
    #     # attributes for connecting to the database
    #     conn = None
    #
    #     # reading the csv file
    #     df = pd.read_csv(csv_path)
    #
    #     # connecting to the database
    #     try:
    #         with psycopg2.connect(
    #                     host = Database_Filler.hostname,
    #                     dbname = Database_Filler.database,
    #                     user = Database_Filler.username,
    #                     password = Database_Filler.pwd,
    #                     port = Database_Filler.port_id) as conn:
    #
    #             with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur: # for writing or reading from database
    #
    #                 # inseting value script
    #                 insert_script  = 'INSERT INTO public.images(file_path , id ,objects , actions) VALUES (%s , %s , %s , %s)'
    #
    #                 # iterating through each row of the dataframe and extracting the necessary info
    #                 for index , row in tqdm(df.iterrows()):
    #
    #                     file_path = self.change_filepath(row["file_path"])
    #                     id = row["id"]
    #                     containing_objects = row["containing_objects"]
    #                     containing_actins = row["containing_captions"]
    #
    #                     insert_list = (str(file_path) , str(id) , str(containing_objects) , str(containing_actins)) # specifing the types , just to make sure ...
    #
    #                     try :
    #                         # inserting each of the songs to the database
    #                         cur.execute(insert_script , insert_list)
    #                         conn.commit()
    #                         # print(f"song id {id} inserted successfully!")
    #
    #                     except psycopg2.IntegrityError: # if the value already exist in the database skip it
    #                         conn.rollback()
    #                         # print(f"Skipping song id {id} as it already exists!")
    #
    #     except Exception as error:
    #         # print(error)
    #         traceback.print_exc()
    #     finally: # close the connection to the database
    #         if conn is not None:
    #             conn.close()
    @db_connection
    def push_image_info(self , conn=None , cur=None , csv_path=None):

        # attributes for connecting to the database
        # conn = None

        # reading the csv file
        # path = csv_path

        # connecting to the database
        try:
            df = pd.read_csv(csv_path)
            # inseting value script
            insert_script  = 'INSERT INTO public.images(file_path , id ,objects , actions) VALUES (%s , %s , %s , %s)'

            # iterating through each row of the dataframe and extracting the necessary info
            for index , row in tqdm(df.iterrows()):

                file_path = self.change_filepath(row["file_path"])
                id = row["id"]
                containing_objects = row["containing_objects"]
                containing_actins = row["containing_captions"]

                insert_list = (str(file_path) , str(id) , str(containing_objects) , str(containing_actins)) # specifing the types , just to make sure ...

                try :
                    # inserting each of the songs to the database
                    cur.execute(insert_script , insert_list)
                    conn.commit()
                    # print(f"song id {id} inserted successfully!")

                except psycopg2.IntegrityError: # if the value already exist in the database skip it
                    conn.rollback()
                    # print(f"Skipping song id {id} as it already exists!")
            return len(df)

        except Exception as error:
            traceback.print_exc()
            return None



    def push_video_info(self , csv_path):

        # attributes for connecting to the database
        conn = None

        # reading the csv file 
        df = pd.read_csv(csv_path)

        # connecting to the database
        try:
            with psycopg2.connect(
                        host = Database_Filler.hostname,
                        dbname = Database_Filler.database,
                        user = Database_Filler.username,
                        password = Database_Filler.pwd,
                        port = Database_Filler.port_id) as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur: # for writing or reading from database

                    # inseting value script
                    insert_script  = 'INSERT INTO public.video(file_path , id , containing_objects , containing_actions) VALUES (%s , %s , %s , %s)'

                    # iterating through each row of the dataframe and extracting the necessary info
                    for index , row in tqdm(df.iterrows()):

                        file_path = self.change_filepath(row["file_path"])
                        id = row["id"]
                        containing_objects = row["containing_objects"]
                        containing_actins = row["containing_actions"]

                        insert_list = (str(file_path) , str(id) , str(containing_objects) , str(containing_actins)) # specifing the types , just to make sure ...

                        try :
                            # inserting each of the songs to the database 
                            cur.execute(insert_script , insert_list)
                            conn.commit()
                            # print(f"song id {id} inserted successfully!")

                        except psycopg2.IntegrityError: # if the value already exist in the database skip it
                            conn.rollback()
                            # print(f"Skipping song id {id} as it already exists!")

        except Exception as error:
            # print(error)
            traceback.print_exc()
        finally: # close the connection to the database
            if conn is not None:
                conn.close() 

if __name__ == '__main__':

    CSV_PATH = r"data/csv/image_info.csv"
    filler = Database_Filler()
    # print(filler.perform_database_operation())
    filler.push_image_info(CSV_PATH)