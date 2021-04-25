# coding:utf-8
from execute.analysis.count_failure_mr import CountFailure
import re

class CountFailurePara(CountFailure):

    def __init__(self,dict):
        super().__init__(dict)
        # {'brightness_-100': 128, 'brightness_-20': 128, 'brightness_-40': 128}
        self.all_para_result=self.init_dict()
        # 错误用例数
        self.para_results_dict={}
        # 识别准确率
        self.para_results_ratio={}

    def init_dict(self):
        temp_dict={}
        for path in self.all_result_dict.keys():
            trans_para=self.get_trans_para_name(path)
            temp_dict[trans_para]=0

        return temp_dict

    def get_trans_para_name(self,path):
        regex=r'.*\\(.*?)_.*?_(.*?)_'
        pattern=re.compile(regex)
        trans=pattern.findall(path)[0][0]
        para=pattern.findall(path)[0][1]
        trans_para=trans+"_"+para

        return trans_para

    def failure_count_para(self):
        blur_dict={}
        for path in self.all_result_dict.keys():
            trans_para = self.get_trans_para_name(path)

            if self.all_result_dict[path] == False:
                self.all_para_result[trans_para] +=1

        self.para_results_dict = self.init_dict2()

        for trans in self.para_results_dict.keys():
            temp = {}
            for fail in self.all_para_result.keys():
                tr = fail.split('_')[0]
                pa = fail.split('_')[1]

                if trans == tr:
                    temp[pa] = self.all_para_result[fail]
                    self.para_results_dict[trans] = temp
        return self.para_results_dict

    def failure_count_para_ratio(self,num_orig):
        self.para_results_ratio=self.para_results_dict.copy()

        for trans in self.para_results_ratio.keys():
            para_dict=self.para_results_ratio[trans]

            for para in para_dict.keys():
                num_success=num_orig-para_dict[para]
                para_acc= num_success/num_orig
                para_dict[para]=1-para_acc


    def init_dict2(self):
        temp_dict={}
        for fail in self.all_para_result.keys():
            tr = fail.split('_')[0]
            temp_dict[tr] = {}
        return temp_dict
