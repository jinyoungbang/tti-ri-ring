from time import time, sleep
from xml.sax import parseString
import cv2
import urllib3
import json
import base64
import sounddevice as sd
import numpy as np
from secrets import ETRI_ACCESS_KEY
from modules.utils import is_user_critical, reconfirm_user_critical
from modules.messages import send_alert_message, send_critical_alert_message

openApiURL = "http://aiopen.etri.re.kr:8000/HumanStatus"
accessKey = ETRI_ACCESS_KEY
IS_PUBLIC_AUTHORITY = True


def main():
    cam = cv2.VideoCapture(0)

    # Initialize variables for time
    previous = time()
    delta = 0
    user_lying_data = []  



    is_pending_user_critical = False  
    threshold = 6
    threshold_above_count = 0

    CHUNK = 1024  
    # audio_data = []
    stream = sd.InputStream()

    # Continue looping through frame
    while True:

        # Get the current time, increase delta and update the previous variable
        current = time()
        delta += current - previous
        previous = current
        critical_message_sent = False

        ret, img = cam.read()
        cv2.imshow("frame", img)
        cv2.waitKey(1)

        
        if is_pending_user_critical:
            stream.start()
            indata, overflowed = stream.read(CHUNK)
            volume_norm = np.linalg.norm(indata) * 10
            if volume_norm > threshold:
                threshold_above_count += 1
            
            if threshold_above_count >= 10:
                is_pending_user_critical = False
            
            if delta > 15:
                if not critical_message_sent:
                    send_critical_alert_message()
                    critical_message_sent = True
                delta = -1000
                

        if delta > 15 and not is_pending_user_critical:

            # Reset the time counter
            delta = 0

            # Encode frame into base64 and pass data to API
            retval, buffer = cv2.imencode('.jpg', img)
            type = "jpg"
            imageContents = base64.b64encode(buffer).decode("utf8")

            requestJson = {
                "access_key": accessKey,
                "argument": {
                    "type": type,
                    "file": imageContents
                }
            }

            http = urllib3.PoolManager()
            response = http.request(
                "POST",
                openApiURL,
                headers={"Content-Type": "application/json; charset=UTF-8"},
                body=json.dumps(requestJson)
            )

            response = json.loads(response.data)

            if len(response["return_object"]) < 1 or len(response["return_object"][0]["data"]) < 1:
                continue

            response_data = response["return_object"][0]["data"][1]

            if len(response_data) == 1:
                print(response_data)
                continue

            action = response_data["class"]
            confidence = response_data["confidence"]
            x, y, height, width = response_data["x"], response_data["y"], response_data["height"], response_data["width"]
            print("Action: " + action)
            print("Confidence: " + confidence)
            print("x: " + str(x))
            print("y: " + str(y))
            print("h: " + str(height))
            print("w: " + str(width))
            print("==========")
            user_data = {
                "x": x,
                "y": y,
                "h": height,
                "w": width
            }

            if action == "Lying" and float(confidence) >= 0.60:
                if len(user_lying_data) > 3:
                    user_lying_data.pop(0)
                user_lying_data.append(user_data)
                if is_user_critical(user_lying_data):
                    delta = 0
                    send_alert_message()
                    is_pending_user_critical = True
                    # if reconfirm_user_critical():
                    #     send_critical_alert_message()
                    user_lying_data.clear()
            else:
                user_lying_data.clear()

if __name__ == '__main__':
    main()