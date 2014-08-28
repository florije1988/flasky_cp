# -*- coding: utf-8 -*-
__author__ = 'florije'


def decorate(func):
    print("in decorate function, decorating", func.__name__)

    def wrapper_func(*args):
        print("Executing", func.__name__)
        return func(*args)
    return wrapper_func


def myfunction(parameter):
    print(parameter)


if __name__ == '__main__':
    # dicts = {'1': 1, '2': 2}
    # print sorted(dicts.iteritems(), key=lambda dicts: dicts[1], reverse=True)

    # testfunction = decorate(myfunction)
    # print testfunction
    #
    # print testfunction("hello")

    print '<Role {name}>'.format(name='fuboqing')
