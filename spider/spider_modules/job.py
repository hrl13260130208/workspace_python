
import spider.spider_modules.thread_factory as factory
import spider.spider_modules.name_manager as  name_manager
import threading
import logging
import time


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger("logger")
class Job(object):
    def __init__(self,name):
        self.name=name
        self.speed=False
        self.thread_num=0
        self.done_num=0

    def set_pyname(self,pyname):
        '''

        :param pyname:  python文件名
        :return:
        '''
        self.pyname= pyname

    def set_speed(self):
        '''
        设置一个快速模式：
            当程序启动或某个线程结束时，会检查redis中的靠前的url的list大小，若大于1000，
            则再启动几个对应的线程（线程最多同时执行4个）
        :return:
        '''
        self.speed=True

    def submit(self,*threads,pyname=None):
        '''
        提交爬虫

        :param threads: 线程的类名（str）（程序会按输入的顺序执行线程）
        :param pyname:线程所在的python文件名(python文件必须在spider.spider_thread文件夹下)
        :return:
        '''
        if pyname:
            self.pyname=pyname

        if self.pyname==None:
            raise ValueError("请设置python文件名")

        if threads:
            #导入python文件，获取传入线程的class对象，并设置到factory中
            f = __import__("spider.spider_thread."+self.pyname, fromlist=True)

            self.nm = name_manager.Name_Manager(self.name,threads.__len__())
            self.t_factory = factory.Thread_Factor(self.nm)
            for t_name in threads:
                thread=getattr(f,t_name)
                self.t_factory.set_thread(thread)
            self.execut()
        else:
            raise ValueError("请设置要执行的线程名")


    def execut(self):
        '''
        启动线程，并创建一个condition等待线程执行完成（可以根据线程数和url的量来判断是否启用新的线程）

        :return:
        '''
        logger.info("线程启动...")
        self.check_schedule()

        while (True):
            done = self.nm.get_done_value(self.done_num)
            if done == "True":
                if self.done_num == self.t_factory.threads_len()-1:
                    logger.info("爬虫完成，退出！")
                    self.nm.clear_keys()
                    exit(0)
                else:
                    self.done_num += 1
                    # if self.speed:
                    #     self.start_more()
            time.sleep(60)





    def start_more(self):
        '''
        根据线程数和url的量来判断是否启用新的线程
        :param names:
        :return:
        '''
        logger.info("start more threads！")

        list_len=self.nm.get_list_len(self.done_num)
        if list_len >1000:
            while self.thread_num < 4:
                thread=self.t_factory.get_thread(self.done_num)
                self.thread_num += 1
                thread.start()


    def check_schedule(self):
        '''
        当程序重新启动的时候，检查之前程序爬取的进度，然后根据其进度启动对应的线程

        :param names: NameManager对象
        :param num: 线程数
        :param thread: 包含所有线程的list
        :return:
        '''
        if self.nm.is_not_exits():
            logger.info("check_schedule create!")
            self.nm.create()

        num=self.t_factory.threads_len()

        for i in range(num):
            done = self.nm.get_done_value(i)

            if done == "True":
                self.done_num=i+1
                if i==num:
                    logger.info("spider is done!")
                    exit(0)
            else:
                if i == 0:
                    self.nm.clear_keys()
                    self.nm.create()
                thread=self.t_factory.get_thread(i)
                thread.start()
                # self.thread_num +=1