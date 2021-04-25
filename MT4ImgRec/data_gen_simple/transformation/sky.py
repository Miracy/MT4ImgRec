import cv2
import numpy as np
import re

class SkyBgTrans:
   # src_path,muta_fup,sky_img_path
    def __init__(self,src_path,muta_fup_path,sky_img_path):
        self.src_path=src_path
        self.sky_img_path=sky_img_path
        self.muta_fup_path=muta_fup_path
        self.img_name=self.get_image_name()

    def segment(self):
        for i in range(len(self.sky_img_path)):
            src = cv2.imread(self.src_path)
            sky_img = cv2.imread(self.sky_img_path[i])
            hsv_img = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
            planes = cv2.split(hsv_img)
            planes[2] = cv2.equalizeHist(planes[2])
            mer_img = cv2.merge(planes)

            lower_red = np.array([100, 48, 40])
            upper_red = np.array([124, 255, 255])
            range_img = cv2.inRange(mer_img, lower_red, upper_red)

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
            Erode_img = cv2.erode(range_img, kernel)
            Dilation_img = cv2.dilate(Erode_img, kernel)

            ret, mask = cv2.threshold(Dilation_img, 150, 255, cv2.THRESH_BINARY)
            notmask = cv2.bitwise_not(mask)
            frontpic = cv2.bitwise_and(src, src, mask=notmask)

            sky_resize = cv2.resize(sky_img, (src.shape[1], src.shape[0]))
            backimage = cv2.bitwise_and(sky_resize, sky_resize, mask=mask)
            merge_img = cv2.add(backimage, frontpic)

            cv2.imwrite((self.muta_fup_path + "\\" + "sky"+str(i)+"Mutation" +self.img_name+".jpg"),merge_img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_image_name(self):
        img_name = re.findall(r"(.*)\\(.*).jpg", self.src_path)[0][1]
        return img_name

