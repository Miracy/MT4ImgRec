import re

class TransSetup:
    def __init__(self,image, trans,follow_trans_path):
        self.img_path=image
        self.trans=trans
        self.fu_path=follow_trans_path
        self.img_name = self.get_img_name(self.img_path)

    def get_img_name(self,img_path):
        img_name = re.findall(r"(.*)\\(.*).jpg", img_path)[0][1]
        return img_name

