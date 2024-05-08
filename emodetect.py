import cv2
import torch
from torchvision import transforms
from network import SEResNet
import faceCap


def open(frame):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    loaded_model = SEResNet.se_resnet_18().to(device)
    loaded_model.load_state_dict(torch.load('./checkpoint/SE_ResNet_model2_FER2013_AmdaW_20240411.pth'))
    loaded_model.eval()

    # 定义转换函数，将OpenCV的图像转换为模型可以接受的输入
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(256),
        # transforms.Grayscale(num_output_channels=3),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5077, 0.5077, 0.5077],  #
            std=[0.2119, 0.2119, 0.2119]    #fer2013 fer_mean=0.5077 fer_std=0.2119
        )])

    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    image = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    image=faceCap.faceCap(image)
    img = transform(image).unsqueeze(0).cuda()

    with torch.no_grad():
        outputs = loaded_model(img)
        _, predicted = torch.max(outputs.data, 1)
        emotion = emotion_labels[predicted[0]]

    return emotion 

if __name__ == "__main__":
    open()
