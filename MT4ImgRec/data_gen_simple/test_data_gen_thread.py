# coding:utf-8
from data_gen_simple.transformation.trans_constants import TransformationConstants
from data_gen_simple.transformation.rotation import Rotation
from data_gen_simple.transformation.brightness import Brightness
from data_gen_simple.transformation.gaussian import Gaussian
from data_gen_simple.transformation.bilateral import Bilateral
from data_gen_simple.transformation.median import Median
from data_gen_simple.transformation.averaging import Avergaing
from data_gen_simple.transformation.translation import Translation
from data_gen_simple.transformation.cropping import Cropping
from data_gen_simple.transformation.scale import Scale
import os
import time

class testDataGen:

    def __init__(self, select_trans, image_path, followup_path):
        self.select_trans = select_trans
        self.image_path = image_path
        self.image_list = self.read_image(self.image_path)
        self.fup_path = followup_path
        self.num_trans=len(select_trans)

    def read_image(self, image_path):
        temp = []
        fileList = os.listdir(image_path)
        for image_name in fileList:
            temp.append(image_path + image_name)
        return temp

    def get_select_trans(self):
        for trans in self.select_trans:
            follow_trans_path = self.fup_path + '\\' + trans
            # create file directory
            FileManager.file_exist(self, follow_trans_path)

            self.image_transformation(trans, follow_trans_path)

    def image_transformation(self, trans, follow_trans_path):
        # follow_trans_path: E:\githubAwesomeCode\nlp_pytorch_data\ImageRecognitionData\followup_data\rotation_trans
        begin_time = time.time()

        # 并行时共享变量,执行成功时要有显示
        for image in self.image_list:
            if trans == TransformationConstants.rotation_trans:
                rotation = Rotation(image, trans, follow_trans_path)
                rotation.trans_exe()

            elif trans == TransformationConstants.brightness_trans:
                brightness = Brightness(image, trans, follow_trans_path)
                brightness.trans_exe()

            elif trans == TransformationConstants.gaussian_trans:
                gaussian = Gaussian(image, trans, follow_trans_path)
                gaussian.trans_exe()

            elif trans == TransformationConstants.averaging_trans:
                averaging = Avergaing(image, trans, follow_trans_path)
                averaging.trans_exe()

            elif trans == TransformationConstants.median_trans:
                median = Median(image, trans, follow_trans_path)
                median.trans_exe()

            elif trans == TransformationConstants.scale_trans:
                scale = Scale(image, trans, follow_trans_path)
                scale.trans_exe()

            elif trans == TransformationConstants.bilateral_trans:
                bilateral = Bilateral(image, trans, follow_trans_path)
                bilateral.trans_exe()

            elif trans == TransformationConstants.translation_trans:
                translation = Translation(image, trans, follow_trans_path)
                translation.trans_exe()

            elif trans == TransformationConstants.cropping_trans:
                cropping = Cropping(image, trans, follow_trans_path)
                cropping.trans_exe()

            else:
                raise Exception("wrong or unsupport metamorphic relation")

        end_time = time.time()
        run_time = end_time - begin_time
        print("runtime is: ", run_time)


class FileManager:

    def __init__(self, image_path, test_batch):
        self.image_path = image_path
        self.test_batch = test_batch
        self.followup_path = self.create_fup()

    def create_fup(self):
        path = os.path.abspath(os.path.join(self.image_path, "./..")) + '\\'

        fup_path = path + "followup_data_" + str(self.test_batch)
        return self.file_exist(fup_path)

    def file_exist(self, fup_path):

        isExists = os.path.exists(fup_path)

        if not isExists:
            os.makedirs(fup_path)
            print(fup_path + ' 创建成功')
        else:
            # 如果该文件夹已存在，创建一个后缀为extra的文件夹
            print(fup_path + ' 文件已存在')
            fup_path = fup_path + "_extra"
            os.makedirs(fup_path)
        return fup_path


