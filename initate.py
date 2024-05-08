import threading
import time
import os
from GUI.panel import start_in_thread2
from GUI.Start import main
import json
    
def start_in_thread1():
    from live2d_display_server import main
    main()

def traverFiles():
    matches = []
    for root, dirnames, filenames in os.walk('./dist/assets'):
        for filename in filenames:
            if 'model3.json' in filename:
                matches.append(os.path.join(root, filename).replace('\\', '/').replace('./dist/assets/', ''))
    return matches
def makeDefaultJson(matches):
    default_model = {
        "modelNum": 0,
        "modelAddresss": "hiyori_pro_zh/runtime/hiyori_pro_t11.model3.json"
    }
    model_list = []
    for i in range(len(matches)):  
        model = {
            "modelNum": i,
            "modelAddresss": f"{matches[i]}",
            "modelIcon": "None"
        }
        model_list.append(model)
    # 创建字典
    data = {
        "defaultModel": default_model,
        "modellist": model_list
    }
    # 转换为JSON
    json_data = json.dumps(data, indent=4)
    with open('./dist/default.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    with open('./GUI/default.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
def serve():
    matches = traverFiles()
    makeDefaultJson(matches)
    # start_in_thread1()


if __name__ == '__main__':

    serve()
    t2 = threading.Thread(target=start_in_thread1)
    t2.start()

    time.sleep(5)

    t1 = threading.Thread(target=start_in_thread2)
    t1.start()

