import requests
import PyPDF2
import uuid

url ="https://content.sciendo.com/downloadpdf/journals/acss/14/1/article-p80.xml"
header={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

file="C:/File/download/1.pdf"
def download(url,file):
    data = requests.get(url,headers=header)
    data.encoding = 'utf-8'
    file=open(file,"wb")
    file.write(data.content)


def checkpdf(file):
    pdf=PyPDF2.PdfFileReader(file)
    num=pdf.getNumPages()
    print(num)

print(uuid.uuid3(uuid.NAMESPACE_DNS,"mccqw"))