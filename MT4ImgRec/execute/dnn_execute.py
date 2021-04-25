from PIL import Image
import torch
from torchvision import transforms

class DNN:

    def __init__(self,path):
        self.img_path=path
        self.result=self.test_one()

    def open_one(self):
        img = Image.open(self.img_path)
        return img

    def test_one(self):
        model_path="epoch11.pth"

        net = torch.load(model_path, map_location='cpu')
        net = net.module
        net.eval()

        # 图像预处理，转换成可以作为网络输入的tensor类型
        transform = transforms.Compose([transforms.Resize((512, 512)),transforms.CenterCrop((448, 448)),
                                    transforms.ToTensor(),transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), ])

        # 图像预处理
        img1 = transform(self.open_one())
        img2 = torch.unsqueeze(img1, 0)

        # inference
        out = net(img2)
        out1 = out[0]

        # 加载类标签
        with open('AIR_classes.txt') as f:
            classes = [line.strip() for line in f.readlines()]

        # 对tensor对象out1按行从大到小排序，结果（也是tensor对象）返回给indices
        _, indices = torch.sort(out1, descending=True)
        # 对tensor对象out1按行进行Softmax

        # 返回top1标签及概率
        a = indices[0][0]
        label_name = classes[a]

        return label_name
