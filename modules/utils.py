import sounddevice as sd
import numpy as np
from time import time

def is_user_critical(user_lying_data):
    print("Running: user_lying_data")

    if len(user_lying_data) == 0 or len(user_lying_data) == 1:
        return False

    x_list = [data["x"] for data in user_lying_data]
    y_list = [data["y"] for data in user_lying_data]
    h_list = [data["h"] for data in user_lying_data]
    w_list = [data["w"] for data in user_lying_data]

    x_avg = sum(x_list) / len(x_list)
    y_avg = sum(y_list) / len(y_list)
    h_avg = sum(h_list) / len(h_list)
    w_avg = sum(w_list) / len(w_list)

    x_abs_vals = [abs(x_avg - data) for data in x_list]
    y_abs_vals = [abs(y_avg - data) for data in y_list]
    h_abs_vals = [abs(h_avg - data) for data in h_list]
    w_abs_vals = [abs(w_avg - data) for data in w_list]

    x_abs_vals_avg = sum(x_abs_vals) / len(x_abs_vals)
    y_abs_vals_avg = sum(y_abs_vals) / len(y_abs_vals)
    h_abs_vals_avg = sum(h_abs_vals) / len(h_abs_vals)
    w_abs_vals_avg = sum(w_abs_vals) / len(w_abs_vals)

    print("Averages of abs val---------")
    print(x_abs_vals_avg, y_abs_vals_avg, h_abs_vals_avg, w_abs_vals_avg)
    if x_abs_vals_avg > 150 or y_abs_vals_avg > 150 or h_abs_vals_avg > 150 or w_abs_vals_avg > 150:
        return False
    
    return True

def reconfirm_user_critical():
    CHUNK = 1024  
    # audio_data = []
    stream = sd.InputStream()
    threshold = 6
    threshold_above_count = 0
    previous = time()
    delta = 0
    while True:
        current = time()
        delta += current - previous
        previous = current
        stream.start()
        indata, overflowed = stream.read(CHUNK)
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > threshold:
            threshold_above_count += 1
        
        if threshold_above_count >= 10:
            return False
        
        if delta > 15:
            return True
    
    return True
    

    

