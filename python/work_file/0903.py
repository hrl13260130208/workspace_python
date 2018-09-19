# encoding='utf-8'
import requests
from bs4 import BeautifulSoup
import json

headers = {
	'Accept': 'application/json, text/plain, */*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Authorization': 'Bearer eyJraWQiOiJwcmltb0V4cGxvcmVQcml2YXRlS2V5LU9YIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJQcmltbyIsImp0aSI6IiIsImV4cCI6MTUzNjgwMjc3NSwiaWF0IjoxNTM2NzE2Mzc1LCJ1c2VyIjoiYW5vbnltb3VzLTA5MTJfMDEzOTM1IiwidXNlck5hbWUiOm51bGwsInVzZXJHcm91cCI6IkdVRVNUIiwiYm9yR3JvdXBJZCI6bnVsbCwidWJpZCI6bnVsbCwiaW5zdGl0dXRpb24iOiJPWCIsInZpZXdJbnN0aXR1dGlvbkNvZGUiOiJPWCIsImlwIjoiMTExLjIwNS44OC4yNTAiLCJvbkNhbXB1cyI6ImZhbHNlIiwibGFuZ3VhZ2UiOiIiLCJhdXRoZW50aWNhdGlvblByb2ZpbGUiOiIiLCJ2aWV3SWQiOiJTT0xPIiwiaWxzQXBpSWQiOm51bGwsInNhbWxTZXNzaW9uSW5kZXgiOiIifQ._A2lR2N5JcjteyFVP4l-TwaM79-qv1LFHYZy5tYzDVkaTnKs-IB1vtVt1PU1jXvBcYNd4GS2fgxg24RY-sw78A',
	'Connection': 'keep-alive',
	#Cookie: JSESSIONID=ECF9299D9AC3E0A4A260CF66DDA3B89A; sto-id-%3FSaaS-A_prod%3FPMTEU02.prod.primo.1701-sg=FGHIBAAK; _ga=GA1.3.639271274.1535941090; _gid=GA1.3.143061241.1535941090
	'Host': 'discovered.ed.ac.uk',
	'Referer': 'https://discovered.ed.ac.uk/primo-explore/search?query=sub,contains,Bioinformatics,AND&pfilter=pfilter,exact,books,AND&tab=default_tab&search_scope=default_scope&sortby=rank&vid=44UOE_VU2&mode=advanced&offset=0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
cookies = {
	'JSESSIONID':'CFC58D4794A43969A1DEDDC259AAC658',
	'_gat_UA-44070883-4':'1',
	'_ga':'GA1.3.557800689.1536716370',
	'_gid':'GA1.3.97055629.1536716370',
	'_ga':'GA1.5.557800689.1536716370',
	'_gid':'GA1.5.97055629.1536716370'
}

url ="https://ucl-primo.hosted.exlibrisgroup.com/primo_library/libweb/webservices/rest/primo-explore/v1/pnxs?blendFacetsSeparately=false&getMore=0&inst=UCL&lang=en_US&limit=10&mode=advanced&newspapersActive=false&newspapersSearch=false&offset=10&pcAvailability=false&q=sub,contains,Electronic+Engineering,OR;sub,contains,Electrical+Engineering,AND;facet_pfilter,exact,books,AND&qExclude=&qInclude=&rtaLinks=true&scope=CSCOP_UCL&skipDelivery=Y&sort=rank&tab=local&vid=UCL_VU2"
r = requests.get(url,headers = headers,cookies = cookies)
print ("p",r.content)
j = json.loads(r.content)


for article in j['docs']:
	
	
	if 'date' in article['pnx']['addata']:
		Publication_Date = article['pnx']['addata']['date'][0]
	else:
		Publication_Date = 'empty'
	if 'contributor' in article['pnx']['display']:
		Author = article['pnx']['display']['contributor'][0].replace(';','##')
	else:
		Author = 'empty'	
	if 'title' in article['pnx']['display']:
		Title = article['pnx']['display']['title'][0]
	else:
		Title = 'empty'
	if 'description' in article['pnx']['display']:
		Description = article['pnx']['display']['description'][0]

	else:
		Description = 'empty'
	if 'lds01' in article['pnx']['display']:
		Statement_of_responsibility = article['pnx']['display']['lds01'][0]
		
	else:
		Statement_of_responsibility = 'empty'
	if 'format' in article['pnx']['display']:
		Format = article['pnx']['display']['format'][0]
		
	else:
		Format = 'empty'
	if 'language' in article['pnx']['display']:
		Language = article['pnx']['display']['language'][0]
	else:
		Language = 'empty'
	if 'publisher' in article['pnx']['display']:
		Publisher = article['pnx']['display']['publisher'][0]
		
	else:
		Publisher = 'empty'
	if 'subject' in article['pnx']['display']:
		Subjects = article['pnx']['display']['subject'][0].replace(';','##')
		
	else:
		Subjects = 'empty'
	if 'relation' in article['pnx']['display']:
		Related_Titles = article['pnx']['display']['relation'][0]
		
	else:
		Related_Titles = 'empty'
	if 'source' in article['pnx']['display']:
		Source = article['pnx']['display']['source'][0]
		#print (Source)
	else:
		Source = 'empty'
	if 'type' in article['pnx']['display']:
		Type = article['pnx']['display']['type'][0]
		#print (Type)
	else:
		Type = 'empty'
	if 'identifier' in article['pnx']['display']:
		identifier = article['pnx']['display']['identifier'][0]
		#print (identifier)
	else:
		identifier = 'empty'
	#break
	s = '$$$$'
	string = Publication_Date + s + Author + s + Title + s + Description + s + Statement_of_responsibility + s + Format + s + Language + s + Publisher + s + Subjects + s + Related_Titles + s + Source + s + Type + s + identifier
	string = string.replace('\n','')
	with open('C:/file/ResultFile/ucl.txt','a+',encoding='utf-8') as f:
		f.write(string + '\n')