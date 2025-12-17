def get_safe_info(info_dict, key, default=0):
    val = info_dict.get(key)
    return val if val is not None else default