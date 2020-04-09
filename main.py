import sys		#sys.exit()로 종료하기 위해서
import datetime #파일, 폴더이름에 시간 저장하기 위해서
import os		#폴더를 생성하기 위한 모듈
import time
import urllib.request
import multiprocessing
from bs4 import BeautifulSoup

def ReturnNowTime():
	nowtime = datetime.datetime.now()

	time_y = str(nowtime.year)
	if(nowtime.month<10):
		time_mon = "0"+ str(nowtime.month)
	else:
		time_mon = str(nowtime.month)
		
	if(nowtime.day<10):
		time_d = "0" + str(nowtime.day)
	else:
		time_d = str(nowtime.day)
			
	if(nowtime.hour <10):
		time_h = "0" + str(nowtime.hour)
	else:
		time_h = str(nowtime.hour)

	if(nowtime.minute<10):
		time_m = "0" + str(nowtime.minute)
	else:
		time_m = str(nowtime.minute)
		
	if(nowtime.second<10):
		time_s = "0" + str(nowtime.second)
	else:
		time_s = str(nowtime.second)
		
	day_name_string = time_y + time_mon + time_d +"_"+time_h+time_m+time_s
	return day_name_string
def CutUrl(url_link):
	cuted_url = list(url_link.split("/"))[-1]
	cuted_url = cuted_url.replace("%20", " ")
	cuted_url = cuted_url.replace("%28", "(")
	cuted_url = cuted_url.replace("%29", ")")
	
	return cuted_url
def HttpsToHttps(url_link):
	return "http://" + url_link[8:]
	
#------------main 부분--------------#
while(True):
	print("이미지를 받을 태그를 입력하세요")
	print("*공백을 입력하면 종료됩니다. 공백으로 태그를 구분합니다.")
	print("**규칙에 검색할 태그를 입력하세요. ex) kiyohime berserker")

	searchTags = input()
	searchTagsList = list(searchTags.split())

	rule34_link = "http://rule34.paheal.net/post/list/"

	if (len(searchTagsList) == 0):		#입력한 태그가 없을 경우
		sys.exit()
	elif (len(searchTagsList) == 1):	#입력한 태그가 1개일 경우
		del_index_link = rule34_link + searchTagsList[0] +"/"
		searchLink = rule34_link + searchTagsList[0] +"/1"
	else:								#입력한 태그가 여러개일 경우 태그 사이에 %20을 넣어주는 작업을 한다.
		searchLink = rule34_link
		TagsCount = 1
		for tags in searchTagsList:
			if(TagsCount != len(searchTagsList)):
				searchLink = searchLink + tags +"%20"
			else:
				del_index_link = searchLink + tags +"/"
				searchLink = searchLink + tags +"/1"
			TagsCount+=1

	try:				#html을 파싱함
		response = urllib.request.urlopen(searchLink)
		
	except:		##태그 검색 결과가 없을 경우 태그 입력으로 돌아감
		print("##위 태그 검색 결과가 없습니다. 규칙34에 가서 검색 결과가 있는지 확인하세요##")
		continue
	
	break		##문제 없으면 입력반복 탈출

print("성공적으로 html 코드를 가져왔습니다.")
print("*파이썬이 줠라 느려서 렉걸린거라고 착각할수도 있습니다.")
print("**이 문장이 출력되었다면 잘 작동하고 있는것입니다.")
print("***지금 분석을 시작했으니 조금 많이 기다려주세요. 파이썬이 느린만큼 아주 마아니~")


start_time = time.time()


### 성공적으로 html을 받아왔고 soup에 html로 파싱함
soup = BeautifulSoup(response, 'html.parser')

image_link = []

### 태그 검색 결과가 있을 경우 마지막 페이지 찾기
### last_page 에 마지막 페이지를 저장
last_page_link = soup.find(rel = "last")
last_page_link = last_page_link.get("href","/")
if(len(last_page_link) == len(searchLink)):
	last_page = last_page_link[-1]
else:
	last_page = last_page_link[(len(searchLink) - len(last_page_link))-1:]

### 문자열 형태의 숫자를 정수 형태로 변환
###	추후에 반복문에 사용하기 위함
last_page = int(last_page)
## 디버그용 print(last_page)



### 링크를 리스트에 저장
for anchor in soup.find_all("a", string="Image Only" ):
	image_link.append(HttpsToHttps(anchor.get('href', '/')))


### 다른 페이지에서도 링크 추출 //위에 파싱했던거 계속 반복함
for webindex in range(2, last_page + 1, 1):
	searchLink = del_index_link + str(webindex)
	
	response = urllib.request.urlopen(searchLink)
	soup = BeautifulSoup(response, 'html.parser')
	
	for anchor in soup.find_all("a", string="Image Only" ):
		image_link.append(HttpsToHttps(anchor.get('href', '/')))
	
### url 크롤링 모두 끝 이제 저장하기만 하면 됨	
total_image = len(image_link)
input_tags = ""
for tag_name in searchTagsList:
	input_tags = input_tags + tag_name + " "
input_tags = input_tags[:-1]



print("검색하신 태그 " + input_tags + "의")
print("총 이미지는 {}개 입니다.".format(total_image))

print("이 프로그램이 설치된 경로에 폴더가 생성되고 이미지가 저장됩니다.")
print("아니오를 선택해도 이미지를 다운받을 수 있는 백업 링크 파일은 저장됩니다.")
print("이미지를 다운로드 하시겠습니까? (아니오 = 0/ 예 = 1 or 아무거나)")
are_you_download = input()


### file_time 에 str 타입으로 년도날짜시분초 저장
file_time = ReturnNowTime()

### 텍스트 파일로 링크 저장
openfile = open(file_time + input_tags + ".txt", "w")
image_count = 1
for url in image_link:
	openfile.write(str(image_count) + " " + url + "\n")
	image_count +=1

openfile.close()

### 이미지 다운로드!
if(are_you_download != str(0)):
	### 폴더 생성하기, 상대경로 사용
	bsdir = "./" + file_time + input_tags
	os.mkdir(bsdir)
	print("폴더를 생성했습니다.")


	###리스트의 url 정보를 가지고 이미지 다운로드
	print("이미지 다운로드를 시작합니다.")


	### 진짜 다운로드!
	index_count = 1
	for url in image_link:
		print("now processing {}/{}...".format(index_count, total_image))
		urllib.request.urlretrieve(url, bsdir + "/" + str(index_count) + " " + CutUrl(url))
		index_count += 1

process_time = round(time.time() - start_time, 2)
print("모든 작업을 완료했습니다.")
print("이미지 다운 시간은 총 %.2f초 소요되었습니다." % process_time)
print("이미지 한 장당 평균 %.2f초가 소요되었습니다." % (process_time / int(total_image)))
input("프로그램을 종료하시려면 Enter 키를 눌러주세요.")