import numpy as np
import torch
class EarlyStopper:
    def __init__(self, patience=1, min_delta=0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.min_validation_loss = float('inf')

    def early_stop(self, validation_loss):
        if validation_loss < self.min_validation_loss:
            self.min_validation_loss = validation_loss
            self.counter = 0
        elif validation_loss > (self.min_validation_loss + self.min_delta):
            self.counter += 1
            if self.counter >= self.patience:
                return True
        return False

def mixup_data(x, y, alpha=1.0):
    #随机生成一个 beta 分布的参数 lam，用于生成随机的线性组合，以实现 mixup 数据扩充。
    lam = np.random.beta(alpha, alpha)
    #生成一个随机的序列，用于将输入数据进行 shuffle。
    batch_size = x.size()[0]
    index = torch.randperm(batch_size).cuda()
    #得到混合后的新图片
    mixed_x = lam * x + (1 - lam) * x[index, :]
    #得到混图对应的两类标签
    y_a, y_b = y, y[index]
    return mixed_x, y_a, y_b, lam
