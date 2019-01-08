
import spider.spider_modules.standard_spider as ss
import logging


class Thread_Factor(object):
    def __init__(self,nm):
        self.threads=[]
        self.nm = nm


    def set_thread(self,thread):
        self.threads.append(thread)

    def threads_len(self):
        return self.threads.__len__()

    def get_thread(self,index):
        attr=ss.attr(self.nm,index)
        if index == 0:
            attr.set_start_thread()
        elif index== self.threads_len()-1:
            attr.set_end_thread()

        return self.threads[index](self.nm,attr)






