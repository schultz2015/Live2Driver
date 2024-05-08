import itertools
import random
import numpy as np
import torch
import torch.nn as nn
from tqdm import tqdm
from torch.cuda.amp import GradScaler, autocast
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


class AddNoise(object):
    """
    Args:
        s(float): 噪声率
        p (float): 执行该操作的概率
    """

    def __init__(self, s=0.5, p=0.9):
        assert isinstance(s, float) or (isinstance(p, float))  # 判断输入参数格式是否正确
        self.s = s
        self.p = p

    # transform 会调用该方法
    def __call__(self, img):  # 使得类实例对象可以像调用普通函数那样，以“对象名()”的形式使用并执行对应的代码。
        """
       （PIL全称 Python Imaging Library，是 Python 平台一个功能非常强大而且简单易用的图像处理库。python3叫pillow）
       Args:
            img (PIL Image): PIL Image
        Returns:
            PIL Image: PIL image.
        """
        # 如果随机概率小于 seld.p，则执行 transform
        if random.uniform(0, 1) < self.p:  # random.uniform(参数1，参数2) 返回参数1和参数2之间的任意值
            # 把 image 转为 array
            img_ = np.array(img).copy()
            # 获得 shape，高*宽*通道数
            h, w, c = img_.shape
            # 信噪比
            signal_pct = self.s
            # 噪声的比例 = 1 -信噪比
            noise_pct = (1 - self.s)
            # 选择的值为 (0, 1, 2)，每个取值的概率分别为 [signal_pct, noise_pct/2., noise_pct/2.]
            # 1 为白噪声，2 为 黑噪声
            #numpy.random.choice(a, size=None, replace=True, p=None)解释
            #从a(只要是ndarray都可以，但必须是一维的)中随机抽取数字，并组成指定大小(size)的数组
            #replace:True表示可以取相同数字，False表示不可以取相同数字
            #数组p：与数组a相对应，表示取数组a中每个元素的概率，默认为选取每个元素的概率相同。
            mask = np.random.choice((0, 1, 2), size=(h, w, 1), p=[signal_pct, noise_pct / 2., noise_pct / 2.])
            mask = np.repeat(mask, c, axis=2)
            img_[mask == 1] = 255  # 白噪声
            img_[mask == 2] = 0  # 黑噪声
            # 再转换为 image
            return Image.fromarray(img_.astype('uint8')).convert('RGB')
        # 如果随机概率大于 seld.p，则直接返回原图
        else:
            return img



def accuracy(predictions, labels):
    pred = torch.max(predictions.data, 1)[1]
    rights = pred.eq(labels.data.view_as(pred)).sum()
    return rights, len(labels)



def result(testloader,model):

    model.eval()
    loss_func = nn.CrossEntropyLoss()
    # 进行预测
    val_rights = []
    val_losses = []
    y_true = []
    y_pred = []
    Validbar = tqdm(testloader)
    with torch.no_grad():
        for data, target in Validbar:
            Validbar.set_description("Validing")
            data, target = data.cuda(), target.cuda()
            with autocast():
                outputs = model(data)
                _, predicted = torch.max(outputs.data, 1)
                y_true.extend(target.tolist())
                y_pred.extend(predicted.tolist())

                target=target.long()
                right = accuracy(outputs, target)
                val_loss = loss_func(outputs, target)
                val_rights.append(right)
                # 计算测试损失
                val_losses.append(val_loss.item()) 


    avg_val_loss = sum(val_losses) / len(val_losses)  
    val_r = (sum([tup[0] for tup in val_rights]),sum([tup[1] for tup in val_rights])) 
    val_r_cpu=val_r[0].cpu().numpy()/val_r[1]

    # 生成混淆矩阵
    cm = confusion_matrix(y_true, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    cm = cm * 100
    print("精度",val_r_cpu)
    print("损失",avg_val_loss)
    # 可视化混淆矩阵
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar(format='%1.1f%%') 
    tick_marks = np.arange(7)  # 假设有10个类别
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    plt.xticks(tick_marks, emotion_labels, rotation=45)
    plt.yticks(tick_marks, emotion_labels)
    thresh = cm.max() / 2.

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, f'{cm[i, j]:.1f}%',
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return plt



