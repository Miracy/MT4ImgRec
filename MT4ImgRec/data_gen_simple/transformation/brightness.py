import cv2
import numpy as np
from data_gen_simple.transformation.trans_setup import TransSetup

class Brightness(TransSetup):
    def __init__(self, image, trans, follow_trans_path):
        super().__init__(image, trans, follow_trans_path)

    def trans_exe(self):
        c=1
        para=[-100,-80,-60,-40,-20,20,40,60,80,100]
        img=cv2.imread(self.img_path, cv2.IMREAD_COLOR)

        rows, cols, chunnel = img.shape
        blank = np.zeros([rows, cols, chunnel], img.dtype)
        for _ in para:
            dst = cv2.addWeighted(img, c, blank, 1 - c, _)

            cv2.imwrite(self.fu_path+"\\"+self.trans+"_"+str(_)+"_"+self.img_name+".jpg",dst)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
