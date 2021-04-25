from execute.dnn_execute import DNN


def create_result_dict(all_result,fup,check_result):
        all_result[fup]=check_result

def dnn_execute(test_img):
        dnn=DNN(test_img)
        result=dnn.test_one()
        return result





