import cv2
from data_gen_simple.transformation.trans_setup import TransSetup

class Median(TransSetup):
    def __init__(self, image, trans, follow_trans_path):
        super().__init__(image, trans,follow_trans_path)

    def trans_exe(self):
        image=cv2.imread(self.img_path, cv2.IMREAD_COLOR)

        median_para=[3,5]
        for para in median_para:
            blur_median = cv2.medianBlur(image, para)
            cv2.imwrite(self.fu_path+"\\"+self.trans+"_"+str(para)+"_"+self.img_name+".jpg",blur_median)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
