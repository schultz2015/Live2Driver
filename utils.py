import json
import os
def getJson(address):
    # 获取某Live2D模型的setting.json
    settingJson=os.path.join('./dist/assets/', address["model"].split('/')[0]+'/settiing.json')
    with open(settingJson, 'r') as f:
    # 使用 json.load() 函数读取 JSON 数据
        data = json.load(f)
    return data

def getAddress():
    # 读取stageModel.json获得要加载的Live2D模型
    with open('./GUI/stageModel.json', 'r') as f:
        data = json.load(f)

    return data['modelAddresss']