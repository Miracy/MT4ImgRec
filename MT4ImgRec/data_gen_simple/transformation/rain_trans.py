import cv2
import numpy as np
import re

class Rain:
    def __init__(self,img_path,mut_fup_path):
        self.img_path=img_path
        self.mut_fup_path=mut_fup_path
        self.img_name=self.get_image_name()

    def get_image_name(self):
        img_name = re.findall(r"(.*)\\(.*).jpg", self.img_path)[0][1]
        return img_name

    # value 雨滴数
    def get_noise(self, value):
        img = cv2.imread(self.img_path)
        noise = np.random.uniform(0, 256, img.shape[0:2])
        v = value * 0.01
        noise[np.where(noise < (256 - v))] = 0
        k = np.array([[0, 0.1, 0],
                  [0.1, 8, 0.1],
                  [0, 0.1, 0]])

        noise = cv2.filter2D(noise, -1, k)
        return noise

    # length：雨水水痕长度 angle：雨水下落角度  w：雨点粗细
    def rain_blur(self,noise, length, angle, w):

        trans = cv2.getRotationMatrix2D((length / 2, length / 2), angle - 45, 1 - length / 100.0)
        dig = np.diag(np.ones(length))
        k = cv2.warpAffine(dig, trans, (length, length))
        k = cv2.GaussianBlur(k, (w, w), 0)

        blurred = cv2.filter2D(noise, -1, k)

        cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
        blurred = np.array(blurred, dtype=np.uint8)
        return blurred

    # alpha:亮度，值越大亮度越小
    def add_rain(self,rain,alpha):
        img = cv2.imread(self.img_path)
        rain = np.expand_dims(rain, 2)
        rain = np.repeat(rain, 3, 2)

        result = cv2.addWeighted(img, alpha, rain, 1 - alpha, 1)
        cv2.imwrite((self.mut_fup_path + "\\" + "rainMutation" + self.img_name + ".jpg"), result)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


