import traceback

import cv2
import psycopg2
import psycopg2.extras
from functools import wraps

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

    def find_occurrence(self , table , request_objects, request_actions):

        sorted_items = {}
        for item in table:
            score = 0
            objects = item[2]
            action = item[3]
            file_path = item[0]

            object_list = objects.split("_")
            action_list = action.split("_")

            # calculating the highest score
            highest_score = len(object_list) + (len(action_list) // 2)

            for obj_request in request_objects:
                if obj_request in object_list:
                    score += 1

            for act_request in request_actions:
                if act_request in action:
                    score += 1

            sorted_items[file_path] = score

        sorted_items = sorted(sorted_items.items(), key=lambda x: x[1], reverse=True)
        print(sorted_items)
        image_path = sorted_items[0][0]
        image_path = image_path.replace("\\", "/")
        image_path = r"C:\\python\\NLP\\content_searcher\\" + image_path
        image_path = image_path.replace("\\\\", "/")
        print(image_path)
        image = cv2.imread(image_path)

        return image

    @db_connection
    def find_request(self , conn=None , cur=None , objects= None , request_objects=None , request_actions=None):

        try:
            cur.execute('SELECT * FROM public.images')
            table = cur.fetchall()
            image = self.find_occurrence(table , request_objects , request_actions)
            return image

        except Exception as error:
            traceback.print_exc()
            return None


if __name__ == "__main__":
    request_objects = ["woman" ,"camera"]
    request_actions = ["holding_camera"]
    action = Actions()
    image = action.find_request(request_objects=request_objects , request_actions=request_actions)
    cv2.imshow("image" , image)
    cv2.waitKey(0)