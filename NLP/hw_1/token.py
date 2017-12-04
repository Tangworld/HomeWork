# -*- coding: utf-8 -*-

words = []
dic = []
none = []
global length
length = 0

def pre():
    """
    预处理，读取字典内容
    :return: 
    """
    source = open('output.txt')
    lines = source.readlines()
    for line in lines:
        line = line.decode('utf-8')
        split_line = line.split(' ')
        words.append(split_line[0])
        dic.append(line)
    source.close()
    global length
    length = len(words)


def localize(data):
    data = data.decode('utf-8')
    index = -1
    global length

    if data in words:
        for i in range(length):
            if data == words[i]:
                index = i
                break
    return index


def nlp():
    """
    程序入口
    :return: 
    """
    pre()
    while True:
        data = raw_input('>')
        if not data:
            break
        index = localize(data)
        if index != -1:
            print '该单词的信息为：', dic[index]
        else:
            new_index = process(data)
            if new_index == -1:
                print '很遗憾，词库中没有这个单词'
                none.append(data)
            else:
                print '还原后的单词信息为：', dic[new_index]
    print '未登录单词为：'
    for n in none:
        print n


def process(data):
    """
    根据还原规则进行还原
    名词变复数规则：
    1、直接加s
    2、以s,x,sh,ch结尾的加es
    3、以辅音字母+y结尾变y为i加es
    4、以f或fe结尾，变f或fe为v加es
    5、不规则
    :param data: 
    :return: 
    """
    index = -1
    special = {'men': 'man', 'women': 'woman', 'policemen': 'policeman', 'policewomen': 'policewoman', 'mice': 'mouse', 'children': 'child', 'feet': 'foot'
               , 'teeth': 'tooth', 'fish': 'fish', 'people': 'people', 'Chinese': 'Chinese', 'Japanese': 'Japanese', 'heroes': 'hero', 'Negroes': 'Negro'
               , 'tomatoes': 'tomato', 'potatoes': 'potato', 'zeroes': 'zero'}
    if data in special.keys():
        new_data = special[data]
        index = localize(new_data)
        return index
    # 加s
    temp = data[0:-1]
    temp_index = localize(temp)
    if temp_index != -1:
        index = temp_index
        return index
    # 加es
    temp = data[0:-2]
    temp_index = localize(temp)
    if temp_index != -1:
        index = temp_index
        return index
    # 变y为i加es
    temp = data[0:-3]
    temp = temp + 'y'
    temp_index = localize(temp)
    if temp_index != -1:
        index = temp_index
        return index
    # 变f或fe为ves
    temp = data[0:-3]
    temp_f = temp + 'f'
    tempf_index = localize(temp_f)
    if tempf_index != -1:
        index = tempf_index
        return index
    temp_fe = temp + 'fe'
    tempfe_index = localize(temp_fe)
    if tempfe_index != -1:
        index = tempfe_index
        return index
    # 若所有情况都不满足，则返回-1
    return index

if __name__ == '__main__':
    nlp()
