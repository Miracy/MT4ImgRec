import cv2
import numpy as np
from data_gen_simple.transformation.trans_setup import TransSetup

class Translation(TransSetup):
    def __init__(self, image, trans,  follow_trans_path):
        super().__init__(image, trans, follow_trans_path)

    def trans_exe(self):
        image=cv2.imread(self.img_path, cv2.IMREAD_COLOR)

        height, width = image.shape[:2]
        x=[20,30,40,50,60,70,80,90,100,110]
        for para in x:

            M = np.float32([[1,0,para],[0,1,para]])
            dst = cv2.warpAffine(image, M, (width, height))

            cv2.imwrite(self.fu_path+"\\"+self.trans+"_"+str(para)+"_"+self.img_name+".jpg",dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
