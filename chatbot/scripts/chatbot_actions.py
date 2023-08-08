import traceback
from collections import defaultdict

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

    # wraper used for connecting to the database
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

    # finding the best image based on the request
    def find_image_occurrence(self , table , request_objects, request_actions):

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

        return image , image_path


    # finding the best image based on the request
    def find_video_occurrence(self , table , request_objects, request_actions):

        sorted_items = {}
        highest_score_frame = "None"
        for item in table:
            score = 0
            file_path = item[0]
            id = item[1]
            all_objects = item[2]
            all_actions = item[3]
            containing_objects = item[4]
            containing_actions = item[5]


            all_objects_list = all_objects.split("_")
            all_actions_list = all_actions.split("_#_")

            # calculating the highest score
            highest_score = len(all_objects_list) + (len(all_actions_list) // 2)
            for obj_request in request_objects:
                if obj_request in all_objects_list:
                    score += 1

            for act_request in request_actions:
                if act_request in all_actions_list:
                    score += 1

            sorted_items[id] = score

        sorted_items = sorted(sorted_items.items(), key=lambda x: x[1], reverse=True)
        print(sorted_items)
        chosen_one_id = sorted_items[0][0]

        for item in table:
            item_id = item[1]
            if item_id == chosen_one_id:
                sorted_frames = defaultdict(int)
                chosen_one_con_obj = item[4]
                chosen_one_con_act = item[5]

                containing_objects_list = []
                containing_actions_list = []
                temp_containing_objects_list = chosen_one_con_obj.split("@")
                temp_containing_actions_list = chosen_one_con_act.split("@")

                for frame_actions in temp_containing_actions_list:
                    containing_actions_list.append(frame_actions.split("___"))

                for frame_objects in temp_containing_objects_list:
                    containing_objects_list.append(frame_objects.split("_"))

                for request in request_objects:
                    for i, objs_list in enumerate(containing_objects_list):
                        if request in objs_list:
                            num = objs_list.count(request)
                            sorted_frames[str(i)] += num

                for request in request_actions:
                    for i, actions_list in enumerate(containing_actions_list):
                        if request in actions_list:
                            num = actions_list.count(request)
                            sorted_frames[str(i)] += num
                sorted_frames = sorted(sorted_frames.items(), key=lambda x: x[1], reverse=True)
                highest_score_frame = sorted_frames[0][0]





        # image_path = sorted_items[0][0]
        # image_path = image_path.replace("\\", "/")
        # image_path = r"C:\\python\\NLP\\content_searcher\\" + image_path
        # image_path = image_path.replace("\\\\", "/")
        # print(image_path)
        # image = cv2.imread(image_path)

        return chosen_one_id , ((int(highest_score_frame) * 120) // 25) - 5 , int(highest_score_frame)

    @db_connection
    def find_image_request(self , conn=None , cur=None , objects= None , request_objects=None , request_actions=None):
        try:
            cur.execute('SELECT * FROM public.images')
            table = cur.fetchall()
            image , image_path = self.find_image_occurrence(table , request_objects , request_actions)
            return image , image_path

        except Exception as error:
            traceback.print_exc()
            return None

    @db_connection
    def find_video_request(self , conn=None , cur=None , objects= None , request_objects=None , request_actions=None):
        try:
            cur.execute('SELECT * FROM public.videos')
            table = cur.fetchall()
            print(table)
            video_name , second , frame = self.find_video_occurrence(table , request_objects , request_actions)
            base_path = r"C:\python\NLP\content_searcher\data\videos"
            video_path = str(base_path + "\\" + video_name)
            print("the name of the video is : " + video_path)
            print("the frame is the frame number : " + str(second) )

            return video_path , second , frame

        except Exception as error:
            traceback.print_exc()
            return None

if __name__ == "__main__":
    request_objects = ["dog" ,"blanket"]
    request_actions = ["lay_blanket"]
    action = Actions()
    video_path , second = action.find_video_request(request_objects=request_objects , request_actions=request_actions)
    # cv2.imshow("image" , image)
