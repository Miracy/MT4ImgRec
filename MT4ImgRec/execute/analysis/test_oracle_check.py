#coding:utf-8

class TestOracle:
    def __init__(self,orig_result,fup_result):
        self.orig_result=orig_result
        self.fup_result=fup_result
        self.pass_or_not=self.check_pass()

    def check_pass(self):
        return self.orig_result==self.fup_result
