# -*- coding: utf-8 -*-
__author__ = 'florije'

if __name__ == '__main__':
    dicts = {'1': 1, '2': 2}
    print sorted(dicts.iteritems(), key=lambda dicts: dicts[1], reverse=True)



