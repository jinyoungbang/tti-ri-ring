from time import time
import cv2
import urllib3
import json
import base64
from secrets import ETRI_ACCESS_KEY

openApiURL = "http://aiopen.etri.re.kr:8000/HumanStatus"
accessKey = ETRI_ACCESS_KEY
			

def main():
    cam = cv2.VideoCapture(0)

    # Initialize variables for time
    previous = time()
    delta = 0

    # Continue looping through frame
    while True:

        # Get the current time, increase delta and update the previous variable
        current = time()
        delta += current - previous
        previous = current

        ret, img = cam.read()

        cv2.imshow("frame", img)
        cv2.waitKey(1)

        # Check if 15 seconds passed
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

            print("[responseCode] " + str(response.status))
            print("[responBody]")
            print(response.data)
            response_data = response.data["return_object"][0]["data"][1]
            action = response_data["class"]
            confidence = response_data["confidence"]
            x, y, height, width = response_data["x"], response_data["y"], response_data["height"], response_data["width"]

if __name__ == '__main__':
    main()