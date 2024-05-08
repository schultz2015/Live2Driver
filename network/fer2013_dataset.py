import h5py
import torch
import numpy as np
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import matplotlib.pyplot as plt
from utils import AddNoise

class FER2013(Dataset):
    """`FER2013 Dataset.
    Args:
        train (bool, optional): If True, creates dataset from training set, otherwise
            creates from test set.
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
    mean,std:
        tensor([0.5077]),tensor([0.2119])
    """
 
    #def __init__(self, split='Training', transform=None):
    def __init__(self, split, transform=None):    
        self.transform = transform
        self.split = split  # training set or test set
        self.data = h5py.File('./data/FER2013.h5', 'r', driver='core')
        # now load the picked numpy arrays
        if self.split == 'Training':
            self.train_data = self.data['Training_pixel']
            self.train_labels = self.data['Training_label']
            self.train_data = np.asarray(self.train_data)
            self.train_data = self.train_data.reshape((28709, 48, 48))
            self.train_data = np.array(self.train_data)
           
 
        elif self.split == 'PublicTest':
            self.PublicTest_data = self.data['PublicTest_pixel']
            self.PublicTest_labels = self.data['PublicTest_label']
            self.PublicTest_data = np.asarray(self.PublicTest_data)
            self.PublicTest_data = self.PublicTest_data.reshape((3589, 48, 48))
            self.PublicTest_data = np.array(self.PublicTest_data)
 
        else  :
            self.PrivateTest_data = self.data['PrivateTest_pixel']
            self.PrivateTest_labels = self.data['PrivateTest_label']
            self.PrivateTest_data = np.asarray(self.PrivateTest_data)
            self.PrivateTest_data = self.PrivateTest_data.reshape((3589, 48, 48))
            self.PrivateTest_data = np.array(self.PrivateTest_data)
 
    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        if self.split == 'Training':
            img, target = self.train_data[index], self.train_labels[index]
        elif self.split == 'PublicTest':
            img, target = self.PublicTest_data[index], self.PublicTest_labels[index]
        else:
            img, target = self.PrivateTest_data[index], self.PrivateTest_labels[index]
 
        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = img[:, :, np.newaxis]   #  np.newaxis的作用是增加一个维度
        img = np.concatenate((img, img, img), axis=2)  #完成多个数组的拼接
        img = Image.fromarray(img)
        if self.transform is not None:
            img = self.transform(img)
 
        return img, target
 
    def __len__(self):
        if self.split == 'Training':
            return len(self.train_data)
        elif self.split == 'PublicTest':
            return len(self.PublicTest_data)
        else :
            return len(self.PrivateTest_data)
         


def stdANDmean():
    dataset = FER2013(split='Training',transform=transforms.ToTensor())
    full_loader = DataLoader(dataset, shuffle=False, num_workers=0)
    N_CHANNELS = 1
    mean = torch.zeros(1)
    std = torch.zeros(1)
    print('==> Computing mean and std..')
    for ind,(inputs, target) in enumerate(full_loader):
        for i in range(N_CHANNELS):
            mean[i] += inputs[:,i,:,:].mean()
            std[i] += inputs[:,i,:,:].std()
    mean.div_(len(dataset))
    std.div_(len(dataset))
    return (mean, std)

def testdata(batch_size):
    mean=0.5077
    std=0.2119
    transform_test_FER2013 = transforms.Compose([
            transforms.Resize(256),
            # transforms.Grayscale(num_output_channels=3),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
            mean=[mean, mean, mean],
            std=[std, std, std])
        ])
    Fer2013Test = FER2013(split='PrivateTest', transform=transform_test_FER2013)
    Fer2013TestLoader = DataLoader(Fer2013Test, batch_size=batch_size , shuffle=True)
    return Fer2013TestLoader

def validdata(batch_size):
    mean=0.5077
    std=0.2119
    transform_test_FER2013 = transforms.Compose([
            transforms.Resize(256),
            # transforms.Grayscale(num_output_channels=3),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
            mean=[mean, mean, mean],
            std=[std, std, std])
        ])
    Fer2013Valid = FER2013(split='PublicTest', transform=transform_test_FER2013)
    Fer2013ValidLoader = DataLoader(Fer2013Valid, batch_size=batch_size , shuffle=True)
    return Fer2013ValidLoader

def traindata(batch_size):
    mean=0.5077
    std=0.2119
    transform_train_FER2013 = transforms.Compose([
            transforms.Resize(256),
            # transforms.Grayscale(num_output_channels=3),
            transforms.RandomResizedCrop(250, scale=(0.8, 1.2)),
            transforms.RandomApply([transforms.ColorJitter(
                brightness=0.5, contrast=0.5, saturation=0.5)], p=0.5),
            transforms.RandomApply(
                [transforms.RandomAffine(0, translate=(0.2, 0.2))], p=0.5),
            transforms.RandomHorizontalFlip(),
            transforms.RandomApply([transforms.RandomRotation(10)], p=0.5),
            # transforms.RandomApply([AddNoise(0.5, p=0.5),], p=0.5),
            transforms.CenterCrop(224), 
            transforms.ToTensor(),
            transforms.Normalize(
            mean=[mean, mean, mean],
            std=[std, std, std]),
            transforms.RandomErasing(p=0.5,scale=(0.02,0.33),ratio=(0.3,3.3),
            value=0,inplace=False), #顺序要在ToTensor之后
        ])
    Fer2013Train = FER2013(split='Training', transform=transform_train_FER2013)
    Fer2013TrainLoader = DataLoader(Fer2013Train, batch_size=batch_size , shuffle=True)
    return Fer2013TrainLoader


if __name__ == '__main__':
    validloader=validdata(1)
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    for index,(data,label) in enumerate (validloader):
        print(emotion_labels[int(label)])
        data = data[0].permute(1, 2, 0).numpy()
        plt.imshow(data)
        plt.show()
    