# -*- coding:utf-8 -*-
"""
软件分析测试课程第一次作业：1、用程序构建代码的抽象语法树；2、比较抽象语法树的相似度
作者：唐士杰
学号：MF1733061
"""
import ast
import difflib


def build_ast(code):
    """
    利用python的ast模块进行抽象语法树的分析
    :param code: 待分析的代码
    :return: 输出分析得到的抽象语法树
    """
    tree = ast.parse(code)
    dump_tree = ast.dump(tree)
    print dump_tree


def get_ast():
    """
    接收用户输入，调用build_ast方法进行处理
    :return: 输出分析结果，若输入的代码不合法则给出错误提示
    """
    code = raw_input("input code>")
    try:
        build_ast(code)
    except Exception,e:
        print "Input correct code please!"
        print


def similarity():
    """
    利用python的difflib模块进行抽象语法树的相似度比较
    思想是比较两棵抽象语法树的字符串相似度
    :return: 两棵抽象语法树的相似度
    """
    a = raw_input("The first piece of code>")
    b = raw_input("The second piece of code>")
    try:
        build_ast(a)
        build_ast(b)
    except Exception,e:
        print "Input correct code please!"
        print
        return
    seq = difflib.SequenceMatcher(None, a, b)
    print "The similarity is: ", seq.ratio()
    print


if __name__ == "__main__":
    while True:
        token = raw_input("What do you want? \n 1.input a piece of code and then get its AST\n 2.Compare the similarity of two pieces of code\n >")
        if token == '1':
            get_ast()
        elif token == '2':
            similarity()
        else:
            print "Wrong command!"
            print
