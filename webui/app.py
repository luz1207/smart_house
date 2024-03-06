import cv2
import json
import base64
from flask import Flask
import mediapipe as mp
from application.model import gesTure
from flask import render_template
from flask import Flask, render_template, Response
from flask import Flask, request, jsonify
from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.iai.v20200303 import iai_client, models


app = Flask(__name__)


camera1 = cv2.VideoCapture(0)
def read_usb_capture():
    while 1:
        ret,frame= camera1.read()
        if not ret:break
        #把获取到的图像格式转换(编码)成流数据，赋值到内存缓存中;
        #主要用于图像数据格式的压缩，方便网络传输
        frame = cv2.flip(frame,1)
        ret1,buffer = cv2.imencode('.jpg',frame)
        #将缓存里的流数据转成字节流
        frame = buffer.tobytes()
        #指定字节流类型image/jpeg
        yield  (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
# frame_interval=0.001    
def detect_faces():  
    ret, frame = camera1.read()
    if not ret:
        return 'no image'

    base64_data = base64.b64encode(cv2.imencode('.jpg', frame)[1])
    base64_code = base64_data.decode()


    try:
        httpProfile = HttpProfile()
        httpProfile.endpoint = "iai.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"
        cred = credential.Credential("AKID1KVku4AMUZhjdPyXu9CD8wY2KWaWK2hB","SoS1Rex8CFWktr9bswqnbHkgO4fRMEAs")
        client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)
        req = models.DetectFaceRequest()

        req.MaxFaceNum = 10
        req.Image = base64_code
        req.NeedFaceAttributes = 1
        req.NeedQualityDetection = 1

        resp = client.DetectFace(req)
        json_data = resp.to_json_string()
        #将图像中的人脸标出来
        # face_num = len(json_data)
        face_info_list = json.loads(json_data)["FaceInfos"]
        face_num = len(face_info_list)    
        data = json.loads(json_data)
        
        for i in range(face_num):
            image_w = data["ImageWidth"]
            image_h = data["ImageHeight"] 
            x = data["FaceInfos"][i]["X"]
            y = data["FaceInfos"][i]["Y"]
            width = data["FaceInfos"][i]["Width"]
            height = data["FaceInfos"][i]["Height"]
            if x + width >=image_w :
                W = image_w
            else:
                W = x+width
            if y + height >= image_h:
                H = image_h
            else:
                H = y+height
                
            cv2.rectangle(frame, (x, y), (W, H), (0, 255, 0), 2)
            # 将图像转换为 base64 编码的字符串
            _, encoded_image = cv2.imencode('.jpg', frame)
            image_data = base64.b64encode(encoded_image).decode()
            response_data = {
                'image': image_data,
                'data_info': json_data
            }

            # 将数据转换为 JSON 格式的字符串
        json_response = json.dumps(response_data)

        return f"data: {json_response}\n\n"
    

        # yield f"data: {json_data}\n\n"

    except TencentCloudSDKException as err:
        print(err)
        
    # time.sleep(frame_interval)

def gesture_recognition():
    x= gesTure()
    return x.Control()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed0')
def video_feed0():
    return Response(gesture_recognition(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect_face')
def detect_face():
    return Response(detect_faces(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)

