import threading
import queue
import time

q=queue.Queue()

done=False
def producer(q,condition):
    global done
    print("producer start..")
    for i in range(10):
        print("p:",i)
        q.put(i)
        time.sleep(1)
        """
        if (condition.acquire()):
            condition.notify_all()
            condition.release()
        """
    while(True):
        if(condition.acquire()):
            done=True
            condition.notify_all()
            condition.release()
            break


def consumer(q,condition):
    global done
    print("consumer start...")
    while (True):
        if(condition.acquire()):
            if  not q.empty():
                print("g:",q.get())
            else:
                if done:
                    break
                condition.wait()
            condition.release()
            time.sleep(2)

class P_Thread(threading.Thread):
    def __init__(self,q,c):
        threading.Thread.__init__(self)
        self.c=c
        self.q=q

    def run(self):
        producer(self.q,self.c)
        a=1/0

class G_Thread(threading.Thread):
    def __init__(self,q,c):
        threading.Thread.__init__(self)
        self.q=q
        self.c=c

    def run(self):
        consumer(self.q,self.c)

class test(object):
    def __init__(self,s=None):
        self.s=s

    def run(self):
        st="sdfdf"
        print( st )
        if (self.s):

            self.s()



def dd(d):
    print(d+"sdfasdf")
    time.sleep(1)

if __name__ == '__main__':


    t=test(dd("df"))
    t.run()

    condition1 = threading.Condition()
    condition2 = threading.Condition()
    q = queue.Queue()
    t1=P_Thread(q,condition1)
    t2=G_Thread(q,condition2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("end")
'''
    producer=threading.Thread(target=producer())
    consumer=threading.Thread(target=consumer())

    producer.start()
    consumer.start()

    #producer.join()
    #consumer.join()

'''