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


# So sánh 2 vector theo cách của bạn anh
def compare_2vector(vector1, vector2):
    vector = vector1 / vector2
    simi = np.average(vector) * 100
    return simi


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
    percents.append(compare_2vector(vectors['s01n001.gfd'], vectors[x]))

plt.plot([_ for _ in range(len(percents))], percents, 'bx')
plt.xlabel('Images')
plt.ylabel('Percents')
plt.show()

# # dist là mảng 2 chiều : [distance, 0/1] : 0 là giống, 1 là khác.
# dists = []
# for x in filenames:
#     for y in filenames:
#         if x[0:3] == y[0:3]:
#             if x != y:
#                 dists.append([get_dist_2vector(vectors[x], vectors[y]), 0])
#         else:
#             dists.append([get_dist_2vector(vectors[x], vectors[y]), 1])
#
# dists = np.array(dists)
# y = dists[:, -1]
#
# # simi là mảng các phần tử giống nhau, diff là mảng các phần tử khác nhau.
# simi = dists[y == 0]
# diff = dists[y == 1]
#
# # ở đây e chỉ vẽ khoảng 600 mẫu đầu tiên.
# RANGE = 600
# plt.plot(simi[:RANGE, 0], 'bx')
# plt.plot(diff[:RANGE, 0], 'rx')
# plt.show()
