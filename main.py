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
	print("*-----               검색할 이미지의 태그를 입력하세요               -----*\n**-----    공백을 입력하면 종료됩니다. 공백으로 태그를 구분해요.    -----**\n***----- rule34에 검색할 태그를 입력하세요. ex) kiyohime berserker -----***")
	searchTags = input(">>")
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
		print("\n##-- 검색 결과가 없습니다. rule34에서 검색 결과가 있는지 확인해보세요. --##\n")
		continue
	
	break		##문제 없으면 입력반복 탈출

print("\n!!   성공적으로 html 코드를 가져왔습니다.   !!\n**** 이후 작업은 시간이 오래걸릴 수 있습니다.\n**** 이 문장이 출력되었다면 프로그램은 잘 작동하는 것입니다.\n**** 이미지 URL을 추출하고 있습니다. 조금 많이 기다려주세요.\n\n작업중...\n")

### 시작시간 생성
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
for anchor in soup.find_all("a", string="Image Only"):
	image_link.append(HttpsToHttps(anchor.get('href', '/')))


### 다른 페이지에서도 링크 추출 //위에 파싱했던거 계속 반복함
for webindex in range(2, last_page + 1, 1):
	searchLink = del_index_link + str(webindex)
	
	response = urllib.request.urlopen(searchLink)
	soup = BeautifulSoup(response, 'html.parser')
	
	for anchor in soup.find_all("a", string="Image Only"):
		image_link.append(HttpsToHttps(anchor.get('href', '/')))
	
### url 크롤링 모두 끝 이제 저장하기만 하면 됨
total_image = len(image_link)
input_tags = ""
for tag_name in searchTagsList:
	input_tags = input_tags + tag_name + " "
input_tags = input_tags[:-1]


print("URL의 추출이 끝났습니다. URL 추출에 걸린 시간은 %.2f초 입니다." % round(time.time() - start_time, 2))
print("검색하신 태그 " + input_tags + "의\n총 이미지는 " + str(total_image) + "개 입니다.\n")

print("이미지는 프로그램이 설치된 경로에 폴더가 생성되고 이미지가 저장됩니다.\n아니오를 선택해도 이미지를 다운받을 수 있는 백업 링크 파일은 저장됩니다.\n이미지를 다운로드 하시겠습니까? (아니오 = 0 / 예 = 1 또는 0이외 입력 후 엔터)")
are_you_download = input(">>")


### file_time 에 str 타입으로 년도날짜시분초 저장
file_time = ReturnNowTime()

### bsdir에 폴더 경로 저장
bsdir = "./" + file_time + " " + input_tags


### 텍스트 파일로 링크 저장
openfile = open(bsdir + ".txt", "w")
image_count = 1
for url in image_link:
	openfile.write(str(image_count) + " " + url + "\n")
	image_count +=1

openfile.close()

print("\n##--텍스트 파일에 이미지 URL 저장을 완료했습니다.!--##")

### 이미지 다운로드!
if(are_you_download != str(0)):
	print("총 이미지는 " + str(total_image) + "개 입니다\n특정 위치부터 이미지를 받으시려면 해당 번호를, 아니라면 1을 입력해주세요.")
	start_index = input(">>")
	user_select_index = 0		### 0 이외의 수일 경우 이미지 다운로드 한 시간 계산을 다르게 함

	### 이미지 다운로드 시간을 계산하기 위한 time()
	download_start_time = time.time()

	### 폴더 생성하기, 상대경로 사용
	os.mkdir(bsdir)
	print("\n##--폴더를 생성했습니다.--##\n이미지 다운로드를 시작합니다.")


	### 다운로드 실패 링크 저장 리스트
	fail_link = []

	### 진짜 다운로드!
	try:
		start_index = int(start_index)							### 문자열 입력시 except로 이동 total_image 보다 클경우 else로 이동
		if (start_index <= total_image and start_index > 0):	### 특정 인덱스부터 다운로드 조건
			user_select_index = (total_image + 1) - start_index
			for k in range(start_index, total_image + 1, 1):
				print("now processing {}/{}...".format(k, total_image))

				try:
					urllib.request.urlretrieve(image_link[k-1], bsdir + "/" + str(k) + " " + CutUrl(image_link[k-1]))
				except:		### 이미지 다운로드를 실패했을 경우 fail_link에 번호와 url을 저장
					fail_link.append(str(k) + " " + image_link[k-1])
					print(str(k) + "번 이미지의 다운로드를 실패했습니다.\nurl: " + image_link[k-1])

		else:
			index_count = 1
			for url in image_link:
				print("now processing {}/{}...".format(index_count, total_image))

				try:
					urllib.request.urlretrieve(url, bsdir + "/" + str(index_count) + " " + CutUrl(url))
				except:		### 이미지 다운로드를 실패했을 경우 fail_link에 번호와 url을 저장
					fail_link.append(str(index_count) + " " + url)
					print(str(index_count) + "번 이미지의 다운로드를 실패했습니다.\nurl: " + url)

				index_count += 1

	except:
		index_count = 1
		for url in image_link:
			print("now processing {}/{}...".format(index_count, total_image))

			try:
				urllib.request.urlretrieve(url, bsdir + "/" + str(index_count) + " " + CutUrl(url))
			except:  ### 이미지 다운로드를 실패했을 경우 fail_link에 번호와 url을 저장
				fail_link.append(str(index_count) + " " + url)
				print(str(index_count) + "번 이미지의 다운로드를 실패했습니다.\nurl: " + url)

			index_count += 1

	### 이미지 다운에 실패한 url이 존재한다면 텍스트 파일로 저장에 실패한 이미지 URL 저장
	if (len(fail_link) != 0):
		print("이미지 다운로드에 실패한 URL이 존재합니다.\n텍스트 파일에 이미지 다운로드에 실패한 URL을 저장합니다.")

		openfile = open(file_time + "Download Fail URL " + input_tags + ".txt", "w")
		openfile.write("URL 길이가 너무 길면 프로그램에서 다운로드가 안될 수 있습니다. 그러므로 아래 URL로 직접 다운로드 부탁드립니다. Download Fail URL Total: " + str(len(fail_link)) + "Images\n")

		for txtdata in fail_link:
			openfile.write(txtdata + "\n")

		openfile.close()

	process_time = round(time.time() - download_start_time, 2)
	print("\n모든 작업을 완료했습니다.\n이미지 다운 시간은 총 %.2f초 소요되었습니다." % process_time)
	if(user_select_index == 0):		##0일 경우 모든 이미지 다운로드
		print("이미지 한 장당 평균 %.2f초가 소요되었습니다." % (process_time / int(total_image)))
	else:							##아닐경우 user_select_index 개 만큼 다운로드
		print("이미지 한 장당 평균 %.2f초가 소요되었습니다." % (process_time / user_select_index))

input("\n프로그램을 종료하시려면 Enter키를 눌러주세요.")