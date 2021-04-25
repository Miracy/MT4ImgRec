# coding:utf-8
import cv2
from data_gen_simple.transformation.trans_setup import TransSetup


class Rotation(TransSetup):

    def __init__(self,image, trans, follow_trans_path):
        super().__init__(image, trans, follow_trans_path)

    def trans_exe(self):
        img=cv2.imread(self.img_path, cv2.IMREAD_COLOR)
        height,width=img.shape[:2]

        rotation_para=[10,20,30,40,50,60,70,80,90,100]
        for para in rotation_para:
            M=cv2.getRotationMatrix2D((width/2.0,height/2.0),para,1)
            rotate=cv2.warpAffine(img,M,(width,height))

            cv2.imwrite(self.fu_path+"\\"+self.trans+"_"+str(para)+"_"+self.img_name+".jpg",rotate)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



