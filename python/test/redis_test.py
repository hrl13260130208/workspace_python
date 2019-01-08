import redis


def clear_all(names):
    for key in r.keys(names.name+"*"):
        r.delete( key )

r=redis.Redis(host="127.0.0.1",port=6379,db=8,decode_responses=True)
'''
for key in r.keys("ccgp-jiangsu*"):
    r.delete(key)
'''
def run():
    print(r.keys())

    for key in r.keys():
        #print(key+" "+r.type(key))
        if r.type(key) == "string":
            print(key+":",r.get(key))
        elif r.type(key) == "list":
            print(key+":",r.lrange(key,0,100))
        elif r.type(key) == "set":
            print(key+":",r.smembers(key))


#r.flushall()

if __name__ == '__main__':
    r.flushall()
    run()
    # print(r.delete("cnpiec_49*"))
    # name="cnpiec_49"
    # keys = r.keys(name + "*")
    # for key in keys:
    #     #if key!=name+"_date" and key!=name+"_set":
    #     r.delete(key)


'''
#r.set("test","python_redis")
print(r["test"])
print(r.get("test"))
print(type(r.get("test")))

r.lpush("list","dfs","fsd","dfsdf","dfs")
print(r.lrange("list",0,10))
r.rpop("list")
print(r.lrange("list",0,10))
print(r.llen("list"))

print(r.lindex("list",3))


r.zadd("redis_test_sss","sdfsdf",1)
r.zadd("redis_test_sss","dfsdf",2)
r.zadd("redis_test_sss","fsdf",3)
r.zadd("redis_test_sss","sdf",4)

print(r.zcard("redis_test_sss"))
print(r.zrank("redis_test_sss",2))
'''
