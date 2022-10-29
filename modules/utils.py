def is_user_critical(user_lying_data):
    if len(user_lying_data) == 0 or len(user_lying_data) == 1:
        return False
    
    x_list = [data["x"] for data in user_lying_data]
    y_list = [data["y"] for data in user_lying_data]
    h_list = [data["h"] for data in user_lying_data]
    w_list = [data["w"] for data in user_lying_data]
    print(x_list)
    x_avg = sum(x_list) / len(x_list)
    y_avg = sum(y_list) / len(y_list)
    h_avg = sum(h_list) / len(h_list)
    w_avg = sum(w_list) / len(w_list)

    if x_avg > 150 or y_avg > 150 or h_avg > 150 or w_avg > 150:
        return False
    
    return True