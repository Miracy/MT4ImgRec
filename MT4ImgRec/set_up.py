# coding:utf-8
from data_gen_simple.test_data_gen_thread import testDataGen
from data_gen_simple.transformation.trans_constants import TransformationConstants
from execute.analysis.count_failure_mr import CountFailure
from execute.analysis.count_failure_para import CountFailurePara
from data_gen_simple.transformation.sky import SkyBgTrans
from data_gen_simple.transformation.rain_trans import Rain

def get_select_trans(select_trans):
    for select in select_trans:
        if select == 'blur_trans':
            select_trans.append(TransformationConstants.gaussian_trans)
            select_trans.append(TransformationConstants.median_trans)
            select_trans.append(TransformationConstants.averaging_trans)
            select_trans.append(TransformationConstants.bilateral_trans)

            select_trans.remove('blur_trans')

    return select_trans

def data_gen(file_mag,select_trans):
    #file_mag = FileManager(image_path, test_batch)
    print("followup_data_path: ", file_mag.followup_path)

    # 衍生测试图像生成
    gen = testDataGen(select_trans, file_mag.image_path, file_mag.followup_path)
    gen.get_select_trans()


def analyze_result_mr(num_orig,result_dict):

    #analysis, failure.trans_failure:每条蜕变关系失败的用例数
    failure_mr=CountFailure(result_dict)

    failure_mr.failure_count()
   # print("trans failure: ", failure_mr.trans_failure)

    # 识别准确率
    failure_mr.failure_ratio(num_orig)

    return failure_mr


def analyze_result_para1(num_orig,result_dict):
    failure_para = CountFailurePara(result_dict)
    failure_para.failure_count_para()
    return failure_para

def analyze_result_para2(num_orig,result_dict):
    failure_para = CountFailurePara(result_dict)
    failure_para.failure_count_para()
    # 识别准确率
    failure_para.failure_count_para_ratio(num_orig)
   # print('para_failure_ratio: ', failure_para.para_results_ratio)

    return failure_para

def sky_bg_transformation(src_path,muta_fup):
    sky_img_path=["sky1.jpg","sky2.jpg"]
    sky_bg=SkyBgTrans(src_path,muta_fup,sky_img_path)
    print("src path: ",src_path)
    sky_bg.segment()
    print("mutation_sky successfully")

def rain_transformation(src_path,muta_fup):
    rain_object=Rain(src_path,muta_fup)
    print("src path: ",src_path)

    noise=rain_object.get_noise(value=450)
    rain = rain_object.rain_blur(noise, length=50, angle=-30, w=3)
    rain_object.add_rain(rain, alpha=0.8)

    print("mutation_rain successfully")