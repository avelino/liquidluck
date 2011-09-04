#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Temp(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError


class Pagination(object):
    def __init__(self, rsts, perpage=30):
        self.allrsts = [rst for rst in rsts]
        self.total = len(self.allrsts)
        self.pages = (self.total - 1)/perpage + 1
        self.perpage = perpage

    def get_current_page(self, page=1):
        start = (page-1) * self.perpage
        end = page * self.perpage
        self.rsts = self.allrsts[start:end]
        if page < self.pages:
            self.next = str(page + 1)
        else:
            self.next = None
        if page > 1:
            self.prev = str(page - 1)
        else:
            self.prev = None
        self.page = page
        return self
