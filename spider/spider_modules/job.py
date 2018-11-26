
import spider.spider_modules.thread_factory as factory
import spider.spider_modules.name_manager as  nm
import threading



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
            当程序启动或某个线程结束时，会检查redis中的靠前的url的list大小，若大于500，
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
            self.t_factory=factory.Thread_Factor()
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
        condition=threading.Condition()
        names=nm.Name_Manager(self.name,self.t_factory.threads_len(),condition)
        self.t_factory.set_names(names)
        print("线程启动...")
        self.check_schedule(names)
        if self.speed:
            try:
                self.start_more(names)
            except SystemExit as e:
                if e.code == 1:
                    print("爬虫即将完成，不在启动新线程！")
                else:
                    e.with_traceback()

        while True:
            condition.acquire()
            print("主线程等待...")
            condition.wait()
            self.thread_num -=1

            if self.speed:
                try:
                    self.start_more(names)
                except SystemExit as e:
                    if e.code == 1:
                        print("爬虫即将完成，不再启动新线程！")
                    else:
                        e.with_traceback()
            print("线程数："+str(self.thread_num))
            if self.thread_num == 0:
                break

        print("爬虫完成，退出！")
        exit(0)

    def start_more(self,names):
        '''
        根据线程数和url的量来判断是否启用新的线程
        :param names:
        :return:
        '''
        print("start_more 执行！")
        while(True):
            if self.done_num == names.get_num():
                exit(1)
            done = names.get_done_name_value(names.get_done_name(self.done_num))
            if  done == "True":
               self.done_num+=1
            else:
                break

        list_len=names.get_list_len(names.get_list_name(self.done_num))
        if list_len >500:
            while self.thread_num < 4:
                thread=self.t_factory.get_thread(self.done_num)
                self.thread_num += 1
                thread.start()


    def check_schedule(self, names):
        '''
        当程序重新启动的时候，检查之前程序爬取的进度，然后根据其进度启动对应的线程

        :param names: NameManager对象
        :param num: 线程数
        :param thread: 包含所有线程的list
        :return:
        '''
        if names.is_not_exits():
            print("check_schedule create")
            names.create()

        num=self.t_factory.threads_len()

        for i in range(num):
            done = names.get_done_name_value(names.get_done_name(i))

            if done == "True":
                self.done_num=i+1
                if i==num:
                    print("spider is done!")
                    exit(0)
            else:
                if i == 0:
                    names.clear_all()
                    names.create()
                thread=self.t_factory.get_thread(i)
                thread.start()
                self.thread_num +=1


    """
    file=None
    python_file_name=""
    class_list={}

    def set_python_file_name(self,name):
        self.python_file_name=name

    def set_class(self,class_):
        self.class_list.setdefault(self.class_list.__len__(),class_)

    def start(self,names):

        if names.is_not_exits():
            print("check_schedule create")
            names.create()

        self.create_thread(names)

        '''        if threadings:
            self.check_schedule(names,threadings.__len__(),threadings)
        else:
            print("请输入要执行的线程！")


    def thread_indexs(self,class_list,names):
        num=[]
        for i in class_list:
            done = names.get_done_name_value(names.get_done_name(i))
            if done == "True":
                pass
            else:
                num.append(i)
        return num
'''

    def create_thread(self,  names):
        spider_file=__import__("spider_modules.spider_thread."+self.python_file_name,fromlist=True)
        for i in self.class_list:
            done = names.get_done_name_value(names.get_done_name(i))
            if done == "True":
                pass
            else:
                spider=getattr(spider_file,self.class_list.get(i))
                spider(names,i,self.class_list.__len__()).start()


    def check_schedule(self,names, num, thread):
        '''
        当程序重新启动的时候，检查之前程序爬取的进度，然后根据其进度启动对应的线程

        :param names: NameManager对象
        :param num: 线程数
        :param thread: 包含所有线程的list
        :return:
        '''
        if names.is_not_exits():
            print("check_schedule create")
            names.create()

        for i in range(num):
            done = names.get_done_name_value(names.get_done_name(i))

            if done == "True":
                pass
            else:
                thread[i].set_num(i)

                if i == 0:
                    self.clear_all(names)
                    names.create()
                    thread[0].set_start_thread()
                    thread[0].start()
                elif i==num-1:
                    thread[i].set_end_thread()
                    thread[i].start()
                else:
                    thread[i].start()

    def clear_all(self,names):
        '''
        清除对应names在redis中的数据
        :param names:
        :return:
        '''
        names.clear_all()
"""