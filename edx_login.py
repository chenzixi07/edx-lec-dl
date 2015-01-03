import urllib,urllib2, cookielib,json,re
from bs4 import BeautifulSoup
from utility import download_video
from utility import vid_id
#==========================================================# website information
home= 'https://www.edx.org'
login_page = 'https://courses.edx.org/login'
dashboard = 'https://www.edx.org/dashboard'
login_app=login_page + "_ajax"
#script ,user_email,user_pswd,keyterm=argv
user_email=raw_input("Enter your email-id ")
user_pswd=raw_input("Enter your password ")
keyterm=raw_input("Enter course key term ")

#===========================================================
print user_email
print user_pswd
print login_app
#===========================================================#for getting response header and cookie information

c = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))
urllib2.install_opener(opener)
response = urllib2.urlopen(login_page)
set_cookie = {}
for cookie in c:
	set_cookie[cookie.name] = cookie.value

#===========================================================# preparing header

headers = {'User-Agent': 'edX-downloader/0.01',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
'Referer': "https://courses.edx.org",
'X-Requested-With': 'XMLHttpRequest',
'X-CSRFToken': set_cookie.get('csrftoken', '') }
csrf=headers['X-CSRFToken']
print "csrf token" +csrf
#===========================================================# creating login data
post_data = urllib.urlencode({
'email' : user_email,
'password' : user_pswd,
'remember':False
}).encode('utf-8')
print post_data
#===========================================================#sending request to login_app ,Method=POST

request = urllib2.Request(login_app, post_data,headers)
response = urllib2.urlopen(request)
print "repsonse code=%d" %response.getcode()
data=response.read().decode('utf-8')
resp=json.loads(data)
#===========================================================# to check the login 

print data

if not resp.get('success',False):
	print "error"
else:
	print "success"

#==========================================================#redirecting to dasboard

req = urllib2.Request(dashboard)
resp = urllib2.urlopen(req)
ans=[]
print "status_code==>%d" %resp.getcode()
#print resp.read().find("ujjwal16")
content=BeautifulSoup(resp)
empty=[]
a_list=content.find_all('a')

for link in a_list:
	x=link.get('href')
	empty.append(x)
for s in empty:
	if (keyterm.lower() in s.lower()) and (("/info" or "/info/") in s.lower()):
		ans.append(s)

if not ans:
	print "Sorry no matches found -restart application"
else:
	ans=list(set(ans))
	print "\n".join(ans)
	index=int(raw_input("Input course link index to select course(index start from 1)"))
	main=str(ans[index-1])
	main=home+main
	print main

	#=======================================================#opening courseware

	c_list=[]
	ans=[]
	course = urllib2.Request(main)
	course_resp = urllib2.urlopen(course)
	#print course_resp.getcode()
	course_material=BeautifulSoup(course_resp)
	a_list=course_material.find_all('a')
	for link in a_list:
		x=link.get('href')
		c_list.append(x)

	print  "========================================"
	for s in c_list:
		if "/courseware" in s:
			ans.append(s)
	access=str(ans[0])
	access=home+access
	print access
	print  "========================================"
	#==========================================================#extracting vedio id
	print "Starting video-id extraction"
	courseware=urllib2.Request(access)
	courseware_resp=urllib2.urlopen(courseware)
	print courseware_resp.getcode()
	content=BeautifulSoup(courseware_resp)
	print "You are on page %s" %content.title.stirng
	material=content.find("nav",{"aria-label":"Course Navigation"})
	week=material.find_all('div')
	link={}
	week_name=[]
	for mat in week:
		key=str(mat.h3.a.string)
		key=key.lstrip()
		key=key.rstrip()
		print "Week Name= %s" %key
		week_name.append(key)
		subchap=mat.ul.find_all('a')
		url=[home+a['href'] for a in subchap]
		link[key]=url
	print link
	print "\n".join(week_name)
	vid_list=[]
	vid_list=vid_list+vid_id(link[week_name[2]])
	#======================================================================#under work
	#for name in week_name:
	#	print "Extraction for %s begins" %name
	#	vid_list=vid_list+vid(link[name])	
	#	print "Extraction for %s complete" %name
	#=====================================================================
	print "\n".join(vid_list)
	xyz=raw_input("Press any key to begin downloading or enter No to exit")
	if xyz.lower()!="no":
		print "\n","video will now get downloaded from vid_list"
		download_video(vid_list)
		print "Thanks for choosing edx-lec-dl"
	else:
		print "Thanks for choosing edx-lec-dl"
	#================================================#end