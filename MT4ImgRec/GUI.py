import os
import random
import shutil

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QTextBrowser
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal, QObject
import matplotlib.pyplot as plt
import numpy as np
import datetime
import re
from threading import Thread

from set_up import get_select_trans
from data_gen_simple.test_data_gen_thread import FileManager
from data_gen_simple.transformation.trans_constants import TransformationConstants
from set_up import data_gen, analyze_result_mr, analyze_result_para1, analyze_result_para2
from execute.execute_set_up import ExecuteSetUp
from execute.execute import dnn_execute, create_result_dict
from execute.analysis.test_oracle_check import TestOracle
from set_up import sky_bg_transformation, rain_transformation



def gen_random_color():  # 生成随机颜色
    color_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  'A', 'B', 'C', 'D', 'E', 'F']
    color = ''
    # 一个以“#”开头的6位十六进制数值表示一种颜色，所以要循环6次
    for i in range(6):
        # random.randint表示产生0~15的一个整数型随机数
        color_number = color_list[random.randint(0, 15)]
        color += color_number
    color = '#' + color
    return color


class Mysignal(QObject):
    text_print = Signal(QTextBrowser, str)

class Main_window(object):
    def __init__(self):
        self.ui = QUiLoader().load("UI.ui")
        self.ui.select_folder_button.clicked.connect(self.select_file)  # 选择文件夹

        # 测试数据扩增模块
        self.ui.seg_mutation_button.clicked.connect(self.seg_mutation)  # 分割变异
        self.ui.fusion_mutation_button.clicked.connect(self.fusion_mutation)  # 融合变异

        # 测试执行模块
        self.ui.all_MT_checkbox.stateChanged.connect(lambda: self.check_all(self.ui.all_MT_checkbox))
        # 全选蜕变关系，把lambda表达式当成槽，自己来传参数
        self.ui.checkbox_group.buttonClicked.connect(lambda: self.check(self.ui.MT1_checkbox, self.ui.MT2_checkbox,
                                                                        self.ui.MT3_checkbox, self.ui.MT4_checkbox,
                                                                        self.ui.MT5_checkbox, self.ui.MT6_checkbox))
        self.ui.gen_deu_img_button.clicked.connect(self.compute_test_batch)  # 生成衍生测试图像
        self.ui.gen_deu_img_button.clicked.connect(self.gen_deu_img)  # 生成衍生测试图像
        self.ui.test_exection_button.clicked.connect(self.execute_test)  # 执行测试

        # 测试结果分析模块
        self.ui.gen_MR_res_button.clicked.connect(self.gen_mr_res)  # 生成蜕变测试分析结果
        self.ui.gen_MR_plot_button.clicked.connect(self.gen_mr_plot)  # 生成蜕变关系-识别准确率图
        self.ui.gen_arg_plot_button.clicked.connect(self.gen_arg_plot)  # 生成各蜕变关系参数-识别准确率图

        self.file_mag = None
        self.execute_batch = None
        self.orig_name_re = r"(.*)\\(.*).jpg"
        self.trans_para_regex = r'.*\\(.*?)_.*?_(.*?)_'
        self.all_result = None
        self.failure_mr = None
        self.failure_para = None; self.failure_para2=None
        self.select_trans = None
        self.select_name_list = []
        self.muta_sky_path=''
        self.muta_rain_path=''
        self.all_test_path=''

        self.ms = Mysignal()  # 实例化对象
        self.ms.text_print.connect(self.print2Gui)




    def print2Gui(self, fb, text):
        fb.append(str(text))
        fb.ensureCursorVisible()

    def get_select_trans_list(self):
        self.select_name_list=[]
        blur_tag = 0
        for select in self.select_trans:
            select_name = select.split('_')[0]
            if select_name in TransformationConstants.blur_list:
                blur_tag = 1
                del select
            else:
                self.select_name_list.append(select_name)
        if blur_tag == 1:
            self.select_name_list.append('blur')

    def select_file(self):
        file_path = QFileDialog.getExistingDirectory(self.ui, "Select the storage path")  # 选择存储路径
        self.ui.path_lineEdit.setText(file_path)

    def file_exist(self,fup_path):
        isExists = os.path.exists(fup_path)
        if not isExists:
            os.makedirs(fup_path)
            print(fup_path + ' Create successfully!')  # 创建成功
        else:
            # 如果该文件夹已存在，创建一个后缀为extra的文件夹
            print(fup_path + ' File already exist!')
            fup_path = fup_path + "_extra"
            os.makedirs(fup_path)
        return fup_path

    # 测试数据扩增模块
    def seg_mutation(self):
        file_path = self.ui.path_lineEdit.text() + '/'
        src_path= os.path.abspath(os.path.join(file_path, "./.")) + '\\'

        path = os.path.abspath(os.path.join(file_path, "./..")) + '\\'
        self.muta_sky_path = path + "MutationSky_followup_" + str(self.compute_test_batch())+"\\"
        print("mutation sky followup path: ",self.muta_sky_path)
        self.file_exist(self.muta_sky_path)

        file_list=os.listdir(src_path)
        for file in file_list:
            img_path=src_path+file
            img_path.replace(r'/','\\')
            sky_bg_transformation(img_path,self.muta_sky_path)
        QMessageBox.information(
            self.ui,
            'Tips',
            'Segmentation mutation has completed！')

    def fusion_mutation(self):
        file_path = self.ui.path_lineEdit.text() + '/'
        src_path = os.path.abspath(os.path.join(file_path, "./.")) + '\\'

        path = os.path.abspath(os.path.join(file_path, "./..")) + '\\'
        self.muta_rain_path = path + "MutationRain_followup_" + str(self.compute_test_batch()) + "\\"
        print("mutation rain followup path: ", self.muta_rain_path)
        self.file_exist(self.muta_rain_path)

        file_list = os.listdir(src_path)
        for file in file_list:
            img_path = src_path + file
            img_path.replace(r'/', '\\')
            rain_transformation(img_path, self.muta_rain_path)
        QMessageBox.information(
            self.ui,
            'Tips',
            'Rainy day effect augmentation has completed！')

    # 测试执行模块
    def check_all(self, all_MT_checkbox):
        if all_MT_checkbox.isChecked():  # 如果点击了全选蜕变关系的复选框
            self.ui.MT1_checkbox.setChecked(True)
            self.ui.MT2_checkbox.setChecked(True)
            self.ui.MT3_checkbox.setChecked(True)
            self.ui.MT4_checkbox.setChecked(True)
            self.ui.MT5_checkbox.setChecked(True)
            self.ui.MT6_checkbox.setChecked(True)
        else:
            self.ui.MT1_checkbox.setChecked(False)
            self.ui.MT2_checkbox.setChecked(False)
            self.ui.MT3_checkbox.setChecked(False)
            self.ui.MT4_checkbox.setChecked(False)
            self.ui.MT5_checkbox.setChecked(False)
            self.ui.MT6_checkbox.setChecked(False)

    def check(self, MT1_checkbox, MT2_checkbox, MT3_checkbox, MT4_checkbox, MT5_checkbox, MT6_checkbox):
        if MT1_checkbox.isChecked() & MT2_checkbox.isChecked() & MT3_checkbox.isChecked() & MT4_checkbox.isChecked() & \
                MT5_checkbox.isChecked() & MT6_checkbox.isChecked():
            self.ui.all_MT_checkbox.setChecked(True)

    def compute_test_batch(self):
        now = datetime.datetime.now()
        path_extra = str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+'_'+str(now.minute)
        return path_extra

    def get_all_test_data(self,file_path):
        orig=os.listdir(file_path)
        for ori in orig:
            shutil.copy(file_path+ori,self.all_test_path)

        if (len(self.muta_sky_path) > 0):
            sky_mut=os.listdir(self.muta_sky_path)
            for sky in sky_mut:
                shutil.copy(self.muta_sky_path+sky,self.all_test_path)

        if (len(self.muta_rain_path) > 0):
            rain_mut = os.listdir(self.muta_rain_path)
            for rain in rain_mut:
                shutil.copy(self.muta_rain_path + rain, self.all_test_path)

    def gen_deu_img(self):
        chosen_MT = []
        check_dict = {'brightness_trans': self.ui.MT1_checkbox.isChecked(), 'rotation_trans': self.ui.MT2_checkbox.isChecked(),
                      'translation_trans': self.ui.MT3_checkbox.isChecked(), 'cropping_trans': self.ui.MT4_checkbox.isChecked(),
                      'scale_trans': self.ui.MT5_checkbox.isChecked(), 'blur_trans': self.ui.MT6_checkbox.isChecked()}
        for key in check_dict:
            if check_dict[key]:
                chosen_MT.append(key)
        file_path = self.ui.path_lineEdit.text() + '\\'  # file_path是原始测试图像的路径

        if check_dict['brightness_trans'] | check_dict['rotation_trans'] | check_dict['translation_trans'] | \
                check_dict['cropping_trans'] | check_dict['scale_trans'] | check_dict['blur_trans'] == 0:
            # 如果没有选择蜕变关系，消息框提示
            QMessageBox.warning(
                self.ui,
                'Tips',
                ' No chosen metamorphic relation！')
        elif file_path == '\\':
            QMessageBox.warning(
                self.ui,
                'Tips',
                'The path of original test image was not selected！')
        else:
            test_batch = self.compute_test_batch()  # test_batch是点击“生成衍生测试图像”button的次数

            if (len(self.muta_sky_path) > 0) or (len(self.muta_rain_path) > 0):
                self.all_test_path = os.path.abspath(
                    os.path.join(file_path, ".\..")) + '\\' + "all_test_data_" + self.compute_test_batch() + "\\"
                self.file_exist(self.all_test_path)

            if (len(self.muta_sky_path) > 0):
                muta_sky_img = os.listdir(self.muta_sky_path)
                if len(muta_sky_img) > 0:
                    self.get_all_test_data(file_path)
                    file_path = self.all_test_path
            elif (len(self.muta_rain_path) > 0):
                muta_rain_img = os.listdir(self.muta_rain_path)
                if len(muta_rain_img) > 0:
                    self.get_all_test_data(file_path)
                    file_path = self.all_test_path

            self.select_trans = get_select_trans(chosen_MT)
            self.file_mag = FileManager(file_path, str(test_batch))
            data_gen(self.file_mag, self.select_trans)
            QMessageBox.information(
                self.ui,
                'Tips',
                'The follow-up test images have been generated！')
        self.ui.ori_deu_res_textBrowser.clear()
        self.ui.mt_res_textBrowser.clear()
        self.ui.MT_result_textBrowser.clear()

    def execute_test(self):
        # flag = False
        QMessageBox.information(
            self.ui,
            'Tips',
            'Start testing！')
        self.execute_batch = ExecuteSetUp(self.file_mag.image_path, self.file_mag.followup_path)
        test_data = self.execute_batch.get_test_pair_dict()

        self.all_result = {}
        def run():
            for orig in test_data.keys():
                orig_result = dnn_execute(orig)
                orig_img_name = re.findall(self.orig_name_re,orig)[0][1]
                orig_show = orig_img_name+".jpg : " + orig_result
                mt_res_show =orig_img_name + ".jpg : "
                print(orig_show)
                self.ms.text_print.emit(self.ui.ori_deu_res_textBrowser, orig_show)
                fup_list = test_data[orig]
                self.ms.text_print.emit(self.ui.mt_res_textBrowser, mt_res_show)
                for fup in fup_list:
                    fup_result = dnn_execute(fup)
                    pattern = re.compile(self.trans_para_regex)
                    trans = pattern.findall(fup)[0][0]
                    para = pattern.findall(fup)[0][1]
                    if trans == 'averaging' or trans == 'gaussian' :
                        real_para = str(para) + '*' + str(para)
                    elif trans == 'bilateral':
                        real_para = "(9,75,75)"
                    else:
                        real_para = para
                    trans_para = trans + "_" + real_para
                    each_result = trans_para+" : " + fup_result+'\t'
                    print(each_result)
                    self.ms.text_print.emit(self.ui.ori_deu_res_textBrowser, each_result)
                    check_result = TestOracle(orig_result, fup_result).pass_or_not
                    print('oracle result: ', check_result)
                    if check_result == True:
                        show_check_result = 'pass'
                    else:
                        show_check_result = 'fail'
                    show_result = trans_para+" : " + show_check_result
                    self.ms.text_print.emit(self.ui.mt_res_textBrowser, show_result)
                    create_result_dict(self.all_result, fup, check_result)
                self.ms.text_print.emit(self.ui.ori_deu_res_textBrowser, "--------------------------------")
                self.ms.text_print.emit(self.ui.mt_res_textBrowser, "--------------------------------")
            self.ms.text_print.emit(self.ui.ori_deu_res_textBrowser, "--------------END-------------")
            self.ms.text_print.emit(self.ui.mt_res_textBrowser, "--------------END-------------")
        t = Thread(target=run)
        t.start()

    # 测试结果分析模块
    def gen_mr_res(self):
        if self.failure_mr!=None:
            self.failure_mr.trans_failure.clear()
            print("yes")

        self.get_select_trans_list()

        trans_failure = {}
        self.failure_mr = analyze_result_mr(self.execute_batch.num_orig, self.all_result)

        if(len(self.failure_mr.trans_failure) != self.select_name_list):
            for trans_name in self.failure_mr.trans_failure.keys():
                if trans_name in self.select_name_list:
                    trans_failure[trans_name]=self.failure_mr.trans_failure[trans_name]

        self.failure_mr.trans_failure=trans_failure.copy()
        print("=== trans failure ===: ", trans_failure)
        print("=== real trans failure ===: ", self.failure_mr.trans_failure)

        self.failure_para=analyze_result_para1(self.execute_batch.num_orig,self.all_result)
        print("=== real para failure ===: ", self.failure_para.para_results_dict)

        para_results_dict=self.failure_para.para_results_dict
        blur_para_result={}
        blur_para_result = self.get_real_para_results(self.failure_para.para_results_dict)
        if len(blur_para_result) > 0:
            for blur_trans in TransformationConstants.blur_list:
                del para_results_dict[blur_trans]
            para_results_dict['blur']=blur_para_result
        print("=== real para failure222 ===: ", para_results_dict)

        result_str=''
        for trans in trans_failure.keys():
            result_str=result_str+"MR: " + trans + '\t' + "num of test cases: " + str(self.execute_batch.num_orig*10)  + '\t' + "Num of failing：" + str(trans_failure[trans]) + '\n'+"parameter：  "
            for para in para_results_dict[trans]:
                print(para)
                if para=='median_3' or para=='median_5':
                    para_result ='\t'+ para + '\t' + "\tNum of failing：" +str(para_results_dict[trans][para])+'\n'
                else:
                    para_result ='\t'+ para + '\t' + "Num of failing：" +str(para_results_dict[trans][para])+'\n'
                print(para_result)
                result_str = result_str+para_result

        self.ui.MT_result_textBrowser.setText(result_str)

    def get_real_para_results(self,para_results_dict):
        blur_trans_failure = {}
        for trans in para_results_dict.keys():
            if trans in TransformationConstants.blur_list:
                para_dict = para_results_dict[trans]
                for para in para_results_dict[trans].keys():
                    blur_trans_failure[trans + "_" + para] = para_dict[para]

        real_blur_trans_failure = {}
        for para in blur_trans_failure.keys():
            real_para = ''
            para_real = para.split('_')[0]
            para_num = para.split('_')[1]
            if para_real == 'averaging' or para_real == 'gaussian':
                real_para = para_real + '_' + str(para_num) + '*' + str(para_num)
                real_blur_trans_failure[real_para] = blur_trans_failure[para]
            elif para_real == 'bilateral':
                real_para = para_real + "_(9,75,75)"
                real_blur_trans_failure[real_para] = blur_trans_failure[para]
            elif para_real == 'median':
                real_para=para_real+'_' + str(para_num)
                real_blur_trans_failure[real_para] = blur_trans_failure[para]

        return real_blur_trans_failure

    def gen_mr_plot(self):

        plt.rcParams['font.family'] = 'sans-serif'  # 设定字体为微软雅黑
        plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
        fig = plt.figure(figsize=(6,5))
        fig.canvas.set_window_title('MR-Error recognition ratio')

        dict={}
        if self.failure_mr==None:
            self.gen_mr_res()

        temp_dict=self.failure_mr.trans_failure_ratio
        print("select_name_list: ", self.select_name_list)
        print('temp_dict:',temp_dict)

        if len(temp_dict)!=len(self.select_name_list):
            for trans_name in self.select_name_list:
                dict[trans_name]=self.failure_mr.trans_failure_ratio[trans_name]

        if len(temp_dict)==len(self.select_name_list) and len(temp_dict)==6:
            dict=self.failure_mr.trans_failure_ratio

        print("ratio dict:",dict)

        x = list(dict.keys())
        y = list(dict.values())
        plt.bar(x, y, color=gen_random_color())
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.title("MR-Error recognition ratio")
        plt.xlabel('MR')
        plt.ylabel('Error recognition ratio')
        plt.show()

    def gen_arg_plot(self):
        global sub
        plt.rcParams['font.family'] = 'sans-serif'  # 设定字体为微软雅黑
        plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
        fig = plt.figure()
        fig.canvas.set_window_title('Parameters of MR-Error recognition ratio')
        self.failure_para2 = analyze_result_para2(self.execute_batch.num_orig, self.all_result)
        para_results_dict=self.failure_para2.para_results_dict

        blur_ratio_result = {}
        blur_ratio_result = self.get_real_para_results(self.failure_para2.para_results_dict)
        if len(blur_ratio_result) > 0:
            for blur_trans in TransformationConstants.blur_list:
                del para_results_dict[blur_trans]
            para_results_dict['blur'] = blur_ratio_result
        print("=== real para ratio ===: ", para_results_dict)
        arg_dict=para_results_dict
        i = 1
        for key, value in arg_dict.items():
            value_keys = []
            for v in value.keys():
                if key == 'blur':
                    value_keys.append(value.keys())
                else:
                    value_keys.append(float(v))
            if len(arg_dict) == 1:
                sub = int("11" + '%d' % i)
                fig.set_size_inches(8, 7)
            elif len(arg_dict) == 2:
                sub = int("12" + '%d' % i)
                fig.set_size_inches(10, 5)
            elif len(arg_dict) == 3 or len(arg_dict) == 4:
                sub = int("22" + '%d' % i)
                fig.set_size_inches(10, 10)
            elif len(arg_dict) == 5 or len(arg_dict) == 6:
                sub = int("23" + '%d' % i)
                fig.set_size_inches(16,9)
            i = i + 1
            plt.subplot(sub)
            plt.bar(range(len(value_keys)), value.values(), align='center', color=gen_random_color())
            plt.xticks(range(len(value_keys)), value.keys(), rotation=25)
            plt.yticks(np.arange(0, 1.1, 0.1))
            plt.xlabel(key)
            plt.ylabel('Error recognition ratio')

        plt.show()



if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('logo.png'))
    stats = Main_window()
    stats.ui.show()
    app.exec_()
