import traceback
import psycopg2
import psycopg2.extras
import pandas as pd
from tqdm import tqdm

class Database_Filler():

    hostname = 'localhost'
    database = 'content_label'
    username = 'postgres'
    pwd = 'arshanelmtalab1398a'
    port_id = 5432

    def __init__(self):
        pass

    def change_filepath(self , head_path):
        base_path = "data/"
        path = (base_path + head_path[8:]).replace("/" , "\\")
        return path


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

    CSV_PATH = r"data\csv\video_info.csv"
    filler = Database_Filler()
    filler.push_video_info(CSV_PATH)