#!/usr/bin/python3

from common import PATH
from random import choice, randint, shuffle
import json

# value range and target path value
targetRangeBegin = 50
targetRangeEnd = 650

targetMaxEnd1 = 660  # difficult
targetMaxEnd2 = 1200  # easy


def getRandomTargetData():
    data = []
    for _ in range(12):
        targetName = choice(PATH)
        if _ % 2 == 0:
            targetValue = targetMaxEnd1
        else:
            targetValue = targetMaxEnd2
        # Paths other than the target path
        easyPath = []
        difficultPath = []
        for item in PATH:
            easy = {}
            difficult = {}
            if item != targetName:
                # easy data
                easy['name'] = item
                easy['value'] = randint(targetRangeBegin, targetRangeEnd)
                easyPath.append(easy)
            else:
                # difficult data
                difficult['name'] = targetName
                difficult['value'] = targetValue
                difficultPath.append(difficult)

        d = {
            'target_name': targetName,
            'target_value': targetValue,
            'easy': easyPath,
            'difficult': difficultPath
        }
        typeAndColor(_, d)
        data.append(d)

    return data


def typeAndColor(index, data):
    if index == 0:
        data['image_type'] = 'column'
        data['color'] = 'text'
    if index == 1:
        data['image_type'] = 'column'
        data['color'] = 'text'
    if index == 2:
        data['image_type'] = 'column'
        data['color'] = 'color'
    if index == 3:
        data['image_type'] = 'column'
        data['color'] = 'color'
    if index == 4:
        data['image_type'] = 'bar'
        data['color'] = 'text'
    if index == 5:
        data['image_type'] = 'bar'
        data['color'] = 'text'
    if index == 6:
        data['image_type'] = 'bar'
        data['color'] = 'color'
    if index == 7:
        data['image_type'] = 'bar'
        data['color'] = 'color'
    if index == 8:
        data['image_type'] = 'pie'
        data['color'] = 'color'
    if index == 9:
        data['image_type'] = 'pie'
        data['color'] = 'color'
    if index == 10:
        data['image_type'] = 'pie'
        data['color'] = 'none'
    if index == 11:
        data['image_type'] = 'pie'
        data['color'] = 'none'


def getData():
    serializeData = []
    targetData = getRandomTargetData()

    for item in targetData:
        data_list = item.get('easy') + item.get('difficult')
        shuffle(data_list)
        _data = {
            'data_type': 'easy' if item.get('target_value') == targetMaxEnd2 else 'difficult',
            'target_name': item.get('target_name'),
            'target_value': item.get('target_value'),
            'image_type': item.get('image_type'),
            'color': item.get('color'),
            'data': data_list
        }
        serializeData.append(_data)

    shuffle(serializeData)

    return serializeData


if __name__ == "__main__":
    data = getData()
    print(json.dumps(data))
