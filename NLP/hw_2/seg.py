# -*- coding: utf-8 -*-
# BMM
# 作者：唐士杰 MF1733061
# 使用逆向最大匹配算法实现中文分词
# 查资料发现逆向最大匹配算法比正向最大匹配算法更为精确，因此使用逆向最大匹配算法
dic = []


def init():
    """
    读文件
    获取中文词典
    :return:
    """
    input = open("dic.txt")
    lines = input.readlines()
    for line in lines:
        line = line.decode("utf8")
        temp = line.split(',')
        dic.append(temp[0])
    # for d in dic:
    #     print d


def if_contain(words):
    """
    判断当前词在词典中是否存在
    :param words:
    :return:
    """
    words = words.decode("utf8")
    flag = False
    for d in dic:
        if d == words:
            flag = True
            break
    return flag


def spl(sentence):
    """
    逆向最大匹配算法的主要实现部分
    从后向前切割字符串，直到切割出的子串与词典中的词匹配
    :param sentence:
    :return:
    """
    result = ''
    words = []

    while len(sentence) > 0:
        except_flag = False
        for i in range(len(sentence), 0, -1):
            temp = sentence.decode("utf8")[:i].encode("utf8")     # 中文字符串切割方式
            flag = if_contain(temp)
            if flag:
                words.append(temp)
                sentence = sentence.decode("utf8")[i:].encode("utf8")
                except_flag = True
                break
        if not except_flag:
            # 判断当前字符串是否在词典中并不存在，若该字符串从头切割到尾都没有词典中的词则认为无法切割并且
            # 词典中不存在，此时直接将该词当成切割后的结果加入结果列表
            words.append(sentence)
            break
    for w in words:
        result += (w + '/')
    return result


def main():
    """
    与用户交互接口
    :return:
    """
    init()
    while True:
        input_str = raw_input(">")
        if not input_str:
            break
        result = spl(input_str)
        print "分词结果为："
        print result


if __name__ == "__main__":
    main()
