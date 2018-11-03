#!/usr/bin/env python
# coding=utf-8

import xmltodict

if __name__ == '__main__':
    # 将xml读出
    with open('file.xml') as fd:
        doc = xmltodict.parse(fd.read())
        print(doc['mydocument']['@has'])  # == u'an attribute'
        print(doc['mydocument']['and']['many'])  # == [u'elements', u'more elements']
        print(doc['mydocument']['plus']['@a'])  # == u'complex'
        print(doc['mydocument']['plus']['#text'])  # == u'element as well'

    # 将字典转换成xml
    with open('out.xml', 'w') as f:
        mydict = {
            'text': {
                '@color': 'red',
                '@stroke': '2',
                '#text': 'This is a test'
            }
        }
        f.write(xmltodict.unparse(mydict))
        """ 生成的xml文件结果如下
        <?xml version="1.0" encoding="utf-8"?>
        <text stroke="2" color="red">This is a test</text>
        """
