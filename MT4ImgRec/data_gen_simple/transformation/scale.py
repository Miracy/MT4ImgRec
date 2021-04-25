import cv2
from data_gen_simple.transformation.trans_setup import TransSetup

class Scale(TransSetup):
    def __init__(self, image, trans, follow_trans_path):
        super().__init__(image, trans, follow_trans_path)

    def trans_exe(self):
        image=cv2.imread(self.img_path, cv2.IMREAD_COLOR)
        scale_para=[0.15,0.3,0.45,0.6,0.75,1.15,1.3,1.45,1.6,1.75]
        for para in scale_para:

            dst=cv2.resize(image, (0, 0), fx=para, fy=para, interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(self.fu_path+"\\"+self.trans+"_"+str(para)+"_"+self.img_name+".jpg", dst)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

