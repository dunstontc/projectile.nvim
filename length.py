"""Just a test."""

# import os
import json
# import pprint

# def most_classes(arg_obj):
#     max_count = 0
#     max_class_teacher = ""
#     for key,value in arg.items():
#         temp_count = len(value)
#         if max_count < temp_count:
#             max_count = temp_count
#             max_class_teacher = key
#     print(max_class_teacher)
#
# most_classes(my_dict)

def get_length(array, attribute):
    max_count = int(0)
    for item in array:
        cur_attr = item[attribute]
        cur_len = len(cur_attr)
        if cur_len > max_count:
            max_count = cur_len
    print(max_count)
    return max_count


candidates = []
with open('/Users/clay/.cache/projectile/bookmarks.json', 'r') as fp:
    config = json.load(fp)
    get_length(config, 'path')
    # for obj in config:
    #     candidates.append({
    #         'abbr': '{0:^15} -- {1:^20} -- {2} -- {3}'.format(
    #             obj['name'],
    #             obj['description'],
    #             obj['path'],
    #             obj['added']
    #         )})
    # return candidates


# pprint.pprint(candidates, width=900)






