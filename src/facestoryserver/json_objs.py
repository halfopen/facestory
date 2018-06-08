# coding: utf-8


class Node:

    def __init__(self, style="", dtype="", contents=None):
        """
            初始化节点数据
        :param style: 样式
        :param dtype: 类型
        :param contents:　内容列表
        """
        self.style = style
        self.contents = contents
        self.dtype = dtype

    def to_dict(self):
        """
            返回 dict
        :return:
        """
        d = dict()
        if len(self.style) > 0:
            d['style'] = self.style
        if len(self.contents) > 0:
            d['contents'] = self.contents
        if len(self.dtype) > 0:
            d['dtype'] = self.dtype
        return d


class Result:

    def __init__(self, title="", more="", detail=""):
        self.title = title
        self.more = more
        self.detail = detail

    def to_dict(self):

        d = dict()
        if len(self.title) > 0:
            d['title'] = self.title
        if len(self.more) > 0:
            d['more'] = self.more
        if len(self.detail) > 0:
            d['detail'] = self.detail
        return d
