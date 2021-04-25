class TransformationConstants:
    # blur transformation
    gaussian_trans='gaussian_trans'
    median_trans='median_trans'
    averaging_trans='averaging_trans'
    bilateral_trans='bilateral_trans'

    rotation_trans='rotation_trans'
    brightness_trans='brightness_trans'
    translation_trans='translation_trans'
    cropping_trans='cropping_trans'
    scale_trans = 'scale_trans'
    background_trans='background_trans'

    image_trans_list=[gaussian_trans,median_trans,averaging_trans,bilateral_trans,rotation_trans,
                      brightness_trans,translation_trans,cropping_trans,scale_trans]

    image_trans_dict={'translation': 0, 'rotation': 0, 'brightness': 0, 'scale':0,'cropping':0,'blur':0}

    blur_list=['gaussian','median','averaging','bilateral']

    blur_trans_list=['gaussian_trans','median_trans','averaging_trans','bilateral_trans']


