from time import time
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

    # Continue looping through frame
    while True:

        # Get the current time, increase delta and update the previous variable
        current = time()
        delta += current - previous
        previous = current

        ret, img = cam.read()
        cv2.imshow("frame", img)
        cv2.waitKey(1)

        if delta > 15:

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

            # if len(response["return_object"][0]) < 2:
            #     continue
            response_data = response["return_object"][0]["data"][1]
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
                    send_alert_message()
                    if reconfirm_user_critical():
                        send_critical_alert_message()
                    user_lying_data.clear()
            else:
                user_lying_data.clear()

if __name__ == '__main__':
    main()