import urllib3
import json
from secrets import ETRI_ACCESS_KEY
import cv2
import numpy as np

def blur_and_send_image(image_data, cv2_image):
    print("Running blurring image process function.")
    openApiURL = "http://aiopen.etri.re.kr:8000/FaceDeID"
    accessKey = ETRI_ACCESS_KEY
    type = "1"
    
    imageContents = image_data
    
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
    face_position_data = response["return_object"]["faces"]

    for fp_data in face_position_data:
        
        img = cv2_image

        x, y = fp_data["x"], fp_data["y"]
        w, h = fp_data["width"], fp_data["height"]

        # Grab ROI with Numpy slicing and blur
        ROI = img[y:y+h, x:x+w]
        blur = cv2.GaussianBlur(ROI, (51,51), 0) 
        img[y:y+h, x:x+w] = blur
    # # Insert ROI back into image
    # img[y:y+h, x:x+w] = blur
    cv2.imwrite("./out.png", img)

