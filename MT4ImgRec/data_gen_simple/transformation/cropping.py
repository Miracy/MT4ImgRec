import cv2
from data_gen_simple.transformation.trans_setup import TransSetup

class Cropping(TransSetup):
    def __init__(self, image, trans,  follow_trans_path):
        super().__init__(image, trans, follow_trans_path)

    def trans_exe(self):
        image=cv2.imread(self.img_path, cv2.IMREAD_COLOR)
        height, width = image.shape[:2]

        cropping_para=[1,2,3,4,5,6,7,8,9,10]
        for para in cropping_para:
            ny =para
            nx=para
            y0 = int(height*(ny/32)); y1 = int(height*((32-ny)/32))
            x0 = int(width * (nx / 32)); x1 = int(width * ((32 - nx) / 32))

            dst=image[y0:y1,x0:x1]
            cv2.imwrite(self.fu_path+"\\"+self.trans+"_"+str(para)+"_"+self.img_name+".jpg", dst)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
