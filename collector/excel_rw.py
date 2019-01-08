import xlwt
import xlrd
from  xlutils import copy
from collector.name_manager import execl_bean,url_manager
import logging



logger = logging.getLogger("logger")
class excels():
    def __init__(self,file_path,um):
        self.file_path=file_path
        self.um=um
        self.values=["SOURCENAME","ISSN","EISSN","WAIBUAID","PINJIE","FULL_URL","ABS_URL","FULL_PATH"]
        self.step=0
        # self.save_path="C:/pdfs/excel.xls"
        self.report_path="C:/pdfs/report.txt"
        self.write_step=2
        self.report_step=3
        self.nums=[]
        self.create()

    def create(self):
        rb = xlrd.open_workbook(self.file_path)
        self.r_sheet = rb.sheet_by_index(0)
        self.wb = copy.copy(rb)
        self.w_sheet = self.wb.get_sheet(0)
        self.init_nums()

    def init_nums(self):
        self.list = self.r_sheet.row_values(0)
        for value in self.values:
            index = self.list.index(value)
            self.nums.append(index)

    def read(self):
        logger.info("读取execl...")

        self.create()

        for row in range(self.r_sheet.nrows-1):
            eb=execl_bean()
            eb.row_num=row+1
            eb.sourcename=self.r_sheet.cell(eb.row_num,self.nums[0]).value
            issn=self.r_sheet.cell(eb.row_num,self.nums[1]).value
            eissn=self.r_sheet.cell(eb.row_num,self.nums[2]).value
            if issn =="":
                eb.eissn=eissn
            elif(eissn == ""):
                eb.eissn=issn
            else:
                eb.eissn=issn+"-"+eissn
            eb.waibuaid=self.r_sheet.cell(eb.row_num,self.nums[3]).value
            eb.pinjie=self.r_sheet.cell(eb.row_num,self.nums[4]).value
            eb.full_url=self.r_sheet.cell(eb.row_num,self.nums[5]).value
            eb.abs_url=self.r_sheet.cell(eb.row_num,self.nums[6]).value
            eb.full_path=self.r_sheet.cell(eb.row_num,self.nums[7]).value
            if self.list.__len__()> self.nums[7]+1:
                page_num=self.r_sheet.cell(eb.row_num,self.nums[7]+1).value
                if page_num:
                    eb.page=int(page_num)

            if not eb.is_done():
                self.um.save_step_names(eb.sourcename,self.step)
                self.um.save(eb,self.step)
        print("execl读取完成。")

    def write(self):
        for sn in self.um.get_sourcenames(self.write_step):
            while (True):
                string = self.um.get_eb(sn)
                if string == None:
                    break
                eb = execl_bean()
                eb.paser(string)

                self.w_sheet.write(eb.row_num,self.nums[5],eb.full_url)
                self.w_sheet.write(eb.row_num,self.nums[6],eb.abs_url)
                self.w_sheet.write(eb.row_num,self.nums[7],eb.full_path)
                self.w_sheet.write(eb.row_num,self.nums[7]+1,eb.page)

        self.wb.save(self.file_path)
        print("Excel写入完成。")

    def report(self):
        file=open(self.report_path,"a+")
        for sn in self.um.get_sourcenames(self.report_step):
            while (True):
                string = self.um.get_eb(sn)
                if string == None:
                    break
                file.write(string+"\n")

        print("report文件写入完成。")


if __name__ == '__main__':
    name="dfsf"
    um = url_manager(name)
    file_path = "C:/Users/zhaozhijie.CNPIEC/Desktop/temp/中信所待补全文清单_20181219..xls"
    ex=excels(file_path,um)
    ex.read()
    ex.write()




