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
    dist = np.linalg.norm(vector.tolist())  # Tính khoảng cách giữa 2 ảnh theo ct Euclid
    return dist


def get_similarity_ratio(vector1, vector2):
    min_arr = [min(vector1[i], vector2[i]) for i in range(len(vector1))]
    max_arr = [max(vector1[i], vector2[i]) for i in range(len(vector1))]
    return sum(min_arr) / sum(max_arr)


def compare_2image(img1, img2):  # Hàm so sánh 2 ảnh.
    dist = get_dist_2vector(img1, img2)  # Tính khoảng cách Euclid giữa 2 ảnh, ảnh càng giống thì dist càng nhỏ.
    simi_percent = 100 * (1 - dist)  # Tính phần trăm độ giống nhau giữa 2 ảnh.
    return simi_percent


# Hiện tại ảnh em đang giải nén ra và để trong thư mục images. Bên anh để ở thư mục nào thì sửa lại  IMAGES_PATH
IMAGES_PATH = './images/=Signatures/=GFD/'

# Tính độ giống nhau của 2 ảnh.

# img1 = input("Image 1: ")  # Nhập vào tên ảnh 1
# img2 = input("Image 2: ")  # Nhập vào tên ảnh 2
img1 = "s04n001.gfd"
img2 = "s08n001.gfd"
vec1 = get_vector(IMAGES_PATH + img1)  # Lấy vector dựa vào ảnh
vec2 = get_vector(IMAGES_PATH + img2)  # Lấy vector dựa vào ảnh.

simi_percent = compare_2image(vec1, vec2)  # Tính độ giống nhau giữa 2 vector
print("The similarity of " + img1 + " and " + img2 + " is: " + str(round(simi_percent, 2)) + "%")

ratio = get_similarity_ratio(vec1, vec2)    # Tính ratio theo công thức cuối.
print("The similarity ratio of " + img1 + " and " + img2 + " is: " + str(round(100 * ratio, 2)) + "%")

