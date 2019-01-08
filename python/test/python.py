import os

path="C:/File/ResultFile/changecode"

for filename in os.listdir(path):
    with open(path+"/"+filename,'r',encoding = 'UTF-8') as f:
        for line in f:
            with open(path+"/gbk"+filename,'a+') as f1:
                f1.write(str(line.encode('gbk',errors="ignore")).replace("b'",'').replace("'",'')+ '\n')





        '''
    #if  not os.path.exists(path+"/gbk_"+filename):
        #os.mknod(path+"/gbk_"+filename)

    f1=open(path+"/gbk_"+filename,"w")
    print("change...")
    for line in file:
        f1.write(str(line.encode('gbk', errors="ignore")).replace("b'", '').replace("'", '') + '\n')
    print("finsh!")
'''