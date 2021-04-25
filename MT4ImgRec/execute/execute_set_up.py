# coding:utf-8
import os
import re
from itertools import chain
import time

class ExecuteSetUp:

    def __init__(self,image_path,followup_path):
        # 原始图像路径
        self.orig_path_list=self.get_path_list(image_path)
        self.num_orig=len(self.orig_path_list)

        self.fup_path=followup_path+"\\"
        self.trans_path_list=self.get_path_list(self.fup_path)

        # 所有衍生测试图像路径
        self.fup_path_list=self.get_fup_path_list()

        self.orig_name_re=r"(.*)\\(.*).jpg"
        self.fup_name_re=r"(.*)_(.*).jpg"

    def get_fup_path_list(self):
        all_fup_path=[]

        for trans in self.trans_path_list:
            followup_path=trans+"\\"
            fup_img_list=self.get_path_list(followup_path)
            all_fup_path.append(fup_img_list)

        return list(chain.from_iterable(all_fup_path))

    def get_img_name(self,orig_path,name_re):
        orig_img_name = re.findall(name_re, orig_path)[0][1]
        return orig_img_name

    def get_path_list(self,image_path):
        path_list=[]
        img_list=os.listdir(image_path)
        for img in img_list:
            path_list.append(image_path+img)
        return path_list

    # 字典方法
    def get_test_pair_dict(self):
        begin_time=time.time()

        test_data={}
        for orig_img in self.orig_path_list:
            test_image=[]
            orig_name=self.get_img_name(orig_img,self.orig_name_re)
            test_data[orig_img]=orig_img

            for fup_img in self.fup_path_list:
                fup_name=self.get_img_name(fup_img,self.fup_name_re)
                if orig_name==fup_name:
                    test_image.append(fup_img)
            test_data[orig_img]=test_image

        endtime=time.time(); runtime=endtime-begin_time
        print("runtime: ", runtime)
        return test_data


