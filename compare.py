import os

import matplotlib.pyplot as plt
import numpy as np


def get_vector(path):
    try:
        img = open(path, 'r').readlines()
        vector = np.array([float(x.strip()) for x in img])
    except IOError:  # Trường hợp đọc file lỗi thì ko xử lý, thông báo lỗi.
        vector = np.array([])
        print('Read file error!')
    return vector


def get_dist_2vector(vector1, vector2):  # Hàm này tính khoảng cách giữa 2 vector sử dụng hàm norm L2 của numpy.
    vector = vector1 - vector2
    dist = np.linalg.norm(vector.tolist())
    return dist


# Hiện tại ảnh em đang giải nén ra và để trong thư mục images. Bên anh để ở thư mục nào thì sửa lại  IMAGES_PATH
IMAGES_PATH = './images/=Signatures/=GFD/'

# Đọc các file trong thư mục
filenames = os.listdir(IMAGES_PATH)

# Chuyển toàn bộ các file thành vector cho vào mảng vector
vectors = {}
for name in filenames:
    vector = get_vector(IMAGES_PATH + name)
    vectors[name] = vector

# So sánh ảnh 1 với các ảnh còn lại và vẽ đồ thị.
percents = []
for x in filenames:
    percents.append(get_dist_2vector(vectors['s05n001.gfd'], vectors[x]))

plt.plot([_ for _ in range(len(percents))], percents, 'r1')
plt.xlabel('Images')
plt.ylabel('Distance')
plt.show()

