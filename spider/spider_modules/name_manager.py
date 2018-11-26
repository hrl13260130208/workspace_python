

import redis
import threading


redis_ = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

class Name_Manager(object):
    '''
    负责管理每一个线程向redis中存入数据的名称与线程之间的锁（condition对象）

    '''



    def __init__(self,name,num,mian_condition):
        '''

        :param name: 整爬虫的名称
        :param num:  整爬虫的线程数
        '''
        self.condition=[]
        self.mian_condition=mian_condition
        self.name=name
        self.num=num
        for i in range(num-1):
            self.condition.append( threading.Condition() )

    def create(self):
        '''
        在redis中创建爬虫需要的名称

        :return:
        '''
        redis_.set(self.name,"True")
        for i in range(self.num):
            if not i==0:
                redis_.rpush(self.name+"_list",self.name+"_list_"+str(i))

            redis_.rpush(self.name + "_done", self.name+"_done_"+str(i))
            redis_.set(self.name+"_done_"+str(i),str(False))

    def get_condition(self,num):
        if num>= self.condition.__len__():
            return None
        else:
            return self.condition[num]

    def get_mian_condition(self):
        return self.mian_condition

    def get_list_name(self,num):
        return redis_.lindex(self.name+"_list",num)

    def get_done_name(self,num):
        '''

        :param num:从0开始计算
        :return:
        '''
        return redis_.lindex(self.name + "_done",num)

    def get_done_name_value(self,name):
        return redis_.get(name)

    def set_done_name(self,done_name,bool):
        redis_.getset(done_name, str(bool))

    def has_next(self,list_name):
        return not  redis_.llen(list_name) == 0


    def put_url_redis(self,name, url):
        redis_.lpush(name, url)

    def get_url_redis(self,name):
        return redis_.rpop(name)

    def clear_all(self):
        '''
        清除对应names在redis中的数据
        :param names:
        :return:
        '''
        for key in redis_.keys(self.name + "*"):
            redis_.delete(key)

    def is_not_exits(self):
        return redis_.get(self.name) == "None"

    def get_list_len(self,name):
        return redis_.llen(name)

    def get_num(self):
        return self.num





