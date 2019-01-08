
import redis
import json

redis_ = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

class conf_bean():
    def __init__(self,sourcename,eissn):
        self.sourcename=sourcename
        self.eissn=eissn

    def get_sourcename(self):
        return self.sourcename

    def get_eissn(self):
        return self.eissn

    def to_string(self):
        pass

    def paser(self,str):
        pass

    def default_name(self):
        return self.get_sourcename()+"_default"



class template_manager():
    def __init__(self):
        self.conf_name="sourcenames"

    def save(self,conf_bean):
        if not redis_.exists(conf_bean.get_sourcename()):
            redis_.sadd(self.conf_name,conf_bean.get_sourcename())
            redis_.sadd(conf_bean.get_sourcename(),conf_bean.default_name())

        redis_.sadd(conf_bean.get_sourcename(),conf_bean.get_eissn())
        redis_.set(conf_bean.get_eissn(),conf_bean.to_string())
        redis_.sadd(conf_bean.default_name(),conf_bean.to_string())

    def get(self,conf_bean):
        return redis_.get(conf_bean.get_eissn())

    def get_default(self,conf_bean):
        return redis_.smembers(conf_bean.default_name())

    def get_conf_name(self):
        return redis_.smembers(self.conf_name)

    def get_eissns(self,sourcename):
        return redis_.smembers(sourcename)

    def is_default_key(self,key):
        '''

        :param key:
        :return:
        '''
        return redis_.type(key) == "set"

    def get_conf_string(self,key):
        return redis_.get(key)


class json_conf_bean(conf_bean):
    def set_conf(self,conf):
        self.conf =conf


    def get_conf(self):
        return self.conf

    def to_string(self):
        return json.dumps(self.conf)

    def paser(self,str):
        self.conf=json.loads(str)


class execl_bean():
    def __init__(self):
        self.row_num=0
        self.sourcename=""
        self.eissn=""
        self.waibuaid=""
        self.pinjie=""
        self.full_url=""
        self.abs_url=""
        self.full_path=""
        self.retry=0
        self.page=-1
        self.err_and_step=""


    def is_done(self):
        return self.full_url !="" and self.abs_url != "" and self.full_path != "" and self.page !=-1

    def to_string(self):
        if self.row_num == 0:
            raise ValueError("row_num 不能为 0！")
        if self.sourcename == "":
            raise ValueError("sourcename不能为空！")
        if self.eissn == "":
            raise ValueError("eissn不能为空！")
        if self.pinjie == "" and self.waibuaid =="":
            raise ValueError("pinjie与waibuaid不能为空！")
        return str(self.row_num)+"#"+self.sourcename+"#"+self.eissn+"#"+self.waibuaid+"#" \
                +self.pinjie+"#"+self.full_url+"#"+self.abs_url+"#"+self.full_path+"#"\
               +str(self.retry)+"#"+str(self.page)+"#"+self.err_and_step

    def paser(self,str):
        args=str.split("#")
        self.row_num = int(args[0])
        self.sourcename = args[1]
        self.eissn =args[2]
        self.waibuaid = args[3]
        self.pinjie = args[4]
        self.full_url = args[5]
        self.abs_url = args[6]
        self.full_path = args[7]
        self.retry=int(args[8])
        self.page = int(args[9])
        self.err_and_step=args[10]

class url_manager():
    def __init__(self,name):
        self.name=name
        self.DONE="True"

    def save_step_names(self,sourcename,step):
        redis_.sadd(self.fix("step", step), self.fix(sourcename, step))

    def save(self,execl_bean,step):
        if step>1:
            self.save_step_names(execl_bean.sourcename,step)
        redis_.lpush(self.fix(execl_bean.sourcename,step),execl_bean.to_string())

    def fix(self,string,step):
        return self.name+"_"+string+"_"+str(step)

    def done_name(self,sourcename,step):
        return self.name+ "_" + sourcename+ "_" + str(step)+"_done"

    def get_sourcenames(self,step):
        return redis_.smembers(self.fix("step",step))

    def get_eb(self,sourcename):
        # print(sourcename+":",redis_.llen(sourcename))
        return redis_.lpop(sourcename)

    def set_done(self,sourcename,step):
        redis_.set(self.done_name(sourcename,step),self.DONE)

    def get_done(self,sourcename,step):
        return redis_.get(self.done_name(sourcename,step))

    def clear(self):
        redis_.delete(self.name+"_*")








def rm():
    keys =  redis_.sscan("Gruyter")
    print(type(keys))
    for key in keys[1]:
        redis_.delete(key)

    redis_.delete("Gruyter")

def query():
    for key in redis_.keys("Gruyter*"):
        print(key)


if __name__ == '__main__':
    tm=template_manager()
    jcb=json_conf_bean("Gruyter","2255-8683-2255-8691")
    # a=tm.get(jcb)
    # print(a)
    # print(type(a))
    b=tm.get_default(jcb)
    for c in b:
        print(c)
        print(type(c))

    """
    jcb=json_conf_bean("Gruyter","2255-8691")
    print(jcb.load())
    print(jcb.conf)
"""

