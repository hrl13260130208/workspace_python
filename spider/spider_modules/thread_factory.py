
import spider.spider_modules.standard_spider as ss

class Thread_Factor(object):
    def __init__(self):
        self.threads=[]

    def set_names(self,names):
        self.names = names

    def set_thread(self,thread):
        self.threads.append(thread)

    def threads_len(self):
        return self.threads.__len__()

    def get_thread(self,index):
        attr=ss.attr(self.names)
        if index == 0:
            attr.set_start_thread()
        elif index== self.threads_len()-1:
            attr.set_end_thread()

        attr.set_put_list_name(index)
        attr.set_put_done_name(index)
        attr.set_put_condition(index)
        attr.set_get_list_name(index)
        attr.set_get_done_name(index)
        attr.set_get_condition(index)

        return self.threads[index](self.names,attr)






