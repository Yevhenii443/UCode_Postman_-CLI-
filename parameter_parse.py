def parameter_parse(params):
    if params is None:
        return None
    else:
        result_dict = dict()
        for i in params:
            temp_list = i.split('=')
            result_dict.update({temp_list[0]: temp_list[1]})

    return result_dict
