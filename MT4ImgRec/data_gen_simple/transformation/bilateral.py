import cv2
from data_gen_simple.transformation.trans_setup import TransSetup

class Bilateral(TransSetup):
    def __init__(self, image, trans,  follow_trans_path):
        super().__init__(image, trans, follow_trans_path)

    def trans_exe(self):
        image = cv2.imread(self.img_path, cv2.IMREAD_COLOR)
        para=[9,75,75]
        blur_bilateral = cv2.bilateralFilter(image, para[0], para[1], para[2])

        cv2.imwrite(self.fu_path+"\\"+self.trans+"_bilateral_"+self.img_name+".jpg",blur_bilateral)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
