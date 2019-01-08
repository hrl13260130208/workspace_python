

import redis
import threading
import time


redis_ = redis.Redis(host="127.0.0.1",port=6379,db=8,decode_responses=True)

class Name_Manager(object):
    '''
    负责管理每一个线程向redis中存入数据的名称与线程之间的锁（condition对象）

    '''
    def __init__(self,name,num):
        '''

        :param name: 整爬虫的名称
        :param num:  整爬虫的线程数
        '''
        self.name=name
        self.num=num
        self.lists=self.name+"_list"
        self.dones=self.name + "_done"


    def create_list_name(self,step):
        return self.name+"_list_"+str(step)

    def create_done_name(self,step):
        return  self.name+"_done_"+str(step)

    def create_set_name(self):
        return self.name + "_set"

    def create_date_name(self):
        return self.name + "_date"

    def create(self):
        '''
        在redis中创建爬虫需要的名称

        :return:
        '''
        redis_.set(self.name,str(True))
        for i in range(self.num):
            if not i==0:
                redis_.rpush(self.lists,self.create_list_name(i))

            redis_.rpush(self.dones, self.create_done_name(i))
            redis_.set(self.create_done_name(i),str(False))

    def get_done_value(self,step):
        return redis_.get(self.create_done_name(step))

    def set_done_name(self,step,bool):
        redis_.getset(self.create_done_name(step), str(bool))

    def has_next(self,step):
        return not  redis_.llen(self.create_list_name(step)) == 0


    def put_url_redis(self,step, url):
        redis_.lpush(self.create_list_name(step), url)

    def get_url_redis(self,step):
        return redis_.rpop(self.create_list_name(step))

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

    def get_list_len(self,step):
        return redis_.llen(self.create_list_name(step))

    def get_num(self):
        return self.num

    def is_increment(self,url):
        num=redis_.sadd(self.create_set_name(),url)
        return num==1

    def get_last_date(self):
        return redis_.get(self.create_date_name())

    def set_last_date(self,date):
        redis_.set(self.create_date_name(),date)

    def create_lock_name(self):
        return self.name+"_lock"

    def get_lock(self):
        return redis_.setnx(self.create_lock_name(),1)

    def release_lock(self):
        redis_.delete(self.create_lock_name())

    def clear_keys(self):
        for key in redis_.keys(self.name+"*"):
            if key!=self.create_set_name() and key!=self.create_date_name():
                redis_.delete(key)


if __name__ == '__main__':

    # print(redis_.smembers("cnpiec_49_set"))

    for key in redis_.keys("cnpiec_48*"):
        redis_.delete(key)
        # print(key+" "+redis_.type(key))
        # if redis_.type(key) == "string":
        #     print(key+":",redis_.get(key))
        # elif redis_.type(key) == "list":
        #     print(key+" size:",redis_.llen(key)," values:",redis_.lrange(key,0,100))
        # elif redis_.type(key) == "set":
        #     print(key+":",redis_.smembers(key))






