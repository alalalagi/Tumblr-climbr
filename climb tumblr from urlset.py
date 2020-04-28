import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
# from cool import cool_func 第一個是py檔名字，第二個是function名字

def true_name(x): #重新命名，處理資料夾違法命名
	for i in [':','\n','?','/','|','*','>','<','=']:
		x = x.replace(i,'')
	return x
def download_all_images(url):
	res = requests.get(url) #這是一個class	#print(res.text) #裡面的text屬性就是html原始碼
	html = BeautifulSoup(res.text,'html.parser') #也是建立class	# print(html.title) #這樣印會含有<title>	# print(html.title.text) #這個就是真正的title

	foldertitle = true_name(html.title.text)
	try: #給tumblr用
		if len(re.search('\d+',url.rpartition('/')[2]).group(0)) == 12: #url.rpartition('/')[2](網址最後一項)是12位數字
			foldertitle = foldertitle+'-'+url.rpartition('/')[2]
	except:
		pass
	# print(foldertitle)
	if not os.path.isdir(os.path.join('Downloadpic',foldertitle)): os.mkdir(os.path.join('Downloadpic',foldertitle))

	# 符合filter規則的弄成一個list
	imageset = tum_img_filter.findall(res.text) 
	# print(type(res.text))
	# imageset = sex_filter.findall(res.text)
	# imageset = alltype_img_filter.findall(res.text)

	#這邊刪除已有大圖的小圖(tumblr)---
	#回傳爬不到的網址到txt
	for img in set(imageset): #set裡面已經刪除重複的東西了		
		ID = re.search('http[s]?://\w+.media.tumblr.com/\w+/(\w+\.(?:jpg|png|gif))',img).group(1) #所有圖檔的檔名 in a list
		# ID = re.search('http[s]?://att.52sex.cc/attachments/forum/\d+/\d+/(\w+\.(?:jpg|png|gif))',img).group(1) 
		# ID = re.search('http[s]?://\S+/(\S+\.(?:jpg|png|gif))',img).group(1) #for all image
		# print(ID)
		try:
			urlretrieve(img,os.path.join('Downloadpic',foldertitle,true_name(ID)))
		except:
			print("GGGGGGGGGGGGGGGGGGG爆炸了:"+url)
			faillist.append(url)
			break
		
if __name__ == '__main__':
	if not os.path.isdir('Downloadpic'):
		os.mkdir('Downloadpic')
	tum_img_filter  = re.compile('http[s]?://\w+.media.tumblr.com/\w+/\w+\.(?:jpg|png|gif)')
	sex_filter = re.compile('http[s]?://att.52sex.cc/attachments/forum/\d+/\d+/\w+\.(?:jpg|png|gif)')
	alltype_img_filter = re.compile('http[s]?://\S+\.(?:jpg|png|gif)')

	faillist = []
	fp = open('urlset.txt','r') #之後要改用剪貼簿  #print(fp.read())	
	for line in fp:  			#等於for url in urlset:
		url = (str(line.strip('\n')))	
		download_all_images(url) #壞掉的會輸出到faillist
		print('Finished-----')
	fp.close()
	print('----------------------------------All process finished----------------------------------')
	print('Fail:')
	print(faillist)
	fo = open("faillist.txt", "w")
	for i in faillist:
		fo.write(i+'\n')
	fo.close()	# 關閉打開的文件

	#影片也要弄,fail
    # def get_video_urls(self,text):
    #     video_urls=re.findall('(?P<video_urls>https://www.tumblr.com/video/[^/]*?/\d+/\d+/)',text)
    #     return video_urls


