import cv2
import face_recognition
import numpy as np
from scipy.spatial import distance
from PIL import ImageFont, ImageDraw, ImageTk, Image
import tkinter as tk
from ultralytics import YOLO
from myfacedb import database
from tkinter import Tk,Label
from datetime import datetime

# 從dlib加載人臉識別模型
face_rec_model = face_recognition.api.face_encodings

# 使用face_recognition獲取人臉嵌入的函數
def get_face_embedding(face_image):
    rgbface = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    #print('face_image', face_image)
    face_embedding = face_rec_model(rgbface)
   #face_embedding = face_rec_model(face_image)
    return face_embedding[0] if len(face_embedding) > 0 else None

# 計算兩個人臉嵌入之間的相似度的函數
def cosine_similarity(embedding1, embedding2):
    return 1 - distance.cosine(embedding1, embedding2)

# 從面部嵌入列表中查找最相似面部的函數
def find_most_similar(target_embedding, face_embeddings):
    similarities = [cosine_similarity(target_embedding, embedding) for embedding in face_embeddings]
    most_similar_index = np.argmax(similarities)
    most_similar_similarity = similarities[most_similar_index]
    #print(similarities)
    return most_similar_index, most_similar_similarity

def put_text_on_image(img, text, position):
    # 定義字體比例、顏色和粗細
    font_scale = 1.5
    color = (0, 255, 0)  # Green color (BGR format)
    thickness = 2
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)

def draw_text(img,text,pos,font_size=20):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    b,g,r,a = 0,255,255,0
    ## Use cv2.FONT_HERSHEY_XXX to write English.
    ## Use simsum.ttc to write Chinese.
    fontpath = "simsun.ttc"     
    font = ImageFont.truetype(fontpath,font_size)
    ##將 numpy array 格式的影像物件轉換為 PIL 影像處理物件的影像格式
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    # print(pos)
    # print(text)
    draw.text(pos,text, font = font, fill = (b, g, r, a))
    img = np.array(img_pil)
    return img

# 捕獲幀、檢測人臉並保存嵌入的功能
def grab_face_and_save_embedding():
 
        ret, frame = cap.read()  
        frame1 = frame.copy()
            # Convert the frame to RGB (face_recognition uses RGB)
        rgb_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame1)
            # Get face locations using face_recognition
        face_locations = face_recognition.face_locations(rgb_frame)
            #print(rgb_frame)
        for face_location in face_locations:
            # Extract face location coordinates (top, right, bottom, left)
            top, right, bottom, left = face_location
            
            # Crop the face region from the frame
            face_image = frame[top:bottom, left:right]
            face_embedding = get_face_embedding(face_image)
            # Get the face embedding using face_recognition
            
            similarity_threshold = 0.93
            if face_embedding is not None:
                target=face_embedding 
                most_similar_index, most_similar_similarity = find_most_similar(target, face_embeddings)
                if most_similar_similarity >= similarity_threshold:
                    id,score=find_most_similar(target,face_embeddings)
                    #put_text_on_image(frame,str(id),(left-20, top-20))
                    frame=draw_text(frame,database[id][0],(left-20, top-20))       
                    target_id = database[id][0]
                #print(target_id)
                                
                else:
                    target_id = '非公司人員'
                #r1.config(text=f"{target_id}")
            else:
                target_id = '非公司人員'
            r1.config(text=f"{target_id}")
            if b1.cget("state") == "active":
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                r2_text = f"{target_id}-下班打卡-{current_time}"
                r2.config(text=r2_text)
                with open("Attendance_record.txt", "a") as file:
                    file.write(r2_text + "\n")
            
            if b2.cget("state") == "active":
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                r2_text = f"{target_id}-上班打卡-{current_time}"
                r2.config(text=r2_text)
                with open("Attendance_record.txt", "a") as file:
                    file.write(r2_text + "\n")

            
        frame2 = Image.fromarray(rgb_frame)
        capture_tk = ImageTk.PhotoImage(image=frame2)
        ui_display.imgtk = capture_tk
        ui_display.configure(image=capture_tk)
        ui_display.after(2, grab_face_and_save_embedding) 
        

if __name__ == "__main__":

    face_embeddings=[]
    #load face db
    
    db_dir='database/'
    
    for key,val in database.items():
        print(database[key])
        face_embeddings.append(np.load(db_dir+database[key][2]))

font_label = ('Arial', 32)
font_button = ('Arial', 24)
font_label2 = ('Arial', 18)
main_window = tk.Tk()
main_window.geometry('700x680')
videoFrame = tk.Frame(main_window,bg = 'white').pack()
cap = cv2.VideoCapture(0)
ui_display = tk.Label(videoFrame)
ui_display.pack()

grab_face_and_save_embedding()

r1 = tk.Label(main_window,text='',font=font_label)
b1 = tk.Button(main_window,text='下班',font=font_button)
b2 = tk.Button(main_window,text='上班',font=font_button)
r2 = tk.Label(main_window,text='',font=font_label2)

b1.place(x=420, y=550)
b2.place(x=220, y=550)
r1.place(x=300, y=495)
r2.place(x=180, y=620)
main_window.update()
main_window.mainloop()

