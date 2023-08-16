from PIL import Image
import numpy as np
import face_recognition
import cv2

face_rec_model = face_recognition.api.face_encodings

def get_face_embedding(face_image):
    rgbface = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    #print('face_image', face_image)
    face_embedding = face_rec_model(rgbface)
    #face_embedding = face_rec_model(face_image)
    return face_embedding[0] if len(face_embedding) > 0 else None


# 讀取圖像
image_path = './database/蔡英文.jpg'  # 請將路徑替換為您的圖像路徑
image = Image.open(image_path)

# 將圖像轉換為NumPy陣列
image_array = np.array(image)

# 將NumPy array轉成embedding格式
face_embedding = get_face_embedding(image_array)
#image_array = np.array(image)
print(face_embedding.shape)
print(face_embedding)


# 保存NumPy陣列為.npy檔案
output_npy_path = 'output_image.npy'  # 請指定輸出的.npy檔案路徑
np.save(output_npy_path, face_embedding)