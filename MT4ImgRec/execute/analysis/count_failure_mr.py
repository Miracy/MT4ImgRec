#coding:utf-8
import re
from data_gen_simple.transformation.trans_constants import TransformationConstants

class CountFailure:

    def __init__(self,dict,):
        self.all_result_dict=dict
        self.trans_failure=TransformationConstants.image_trans_dict
        self.trans_failure_ratio={}

    def failure_count(self):
        for key in self.trans_failure.keys():
            self.trans_failure[key]=0

        for path in self.all_result_dict.keys():

            # path='E:\\githubAwesomeCode\\nlp_pytorch_data\\ImageRecognitionData\\followup_data1_extra\\translation_trans\\translation_trans_90_0063096.jpg'
            # 采用非贪婪的方法，尽可能匹配较少的字符
            result=re.findall(r'.*\\(.*?)_.*?_',path)[0]

            if self.all_result_dict[path] == False:
                if result in TransformationConstants.blur_list:
                    self.trans_failure['blur']+=1
                elif self.all_result_dict[path]==False:
                    self.trans_failure[result]+=1

    def failure_ratio(self,num_orig):

        for trans in self.trans_failure.keys():
            num_failure=self.trans_failure[trans]
            all_test=num_orig*10
            num_success=all_test-num_failure

            self.trans_failure_ratio[trans]=1-num_success/(num_orig*10)

