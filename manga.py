import re
from bs4 import BeautifulSoup
import requests
import shutil
img=[]
print("\nRunning...\n")
for i in range(1,2):
  for j in range(1,200):
    URL = "http://www.mangapanda.com/onepunch-man/{}/{}".format(i,j)
    request = requests.get(URL)
    if request.status_code == 200:
         page = requests.get(URL)
         page_content = BeautifulSoup(page.content,'html.parser')
         row_data=[]
         for row in page_content.findAll('script',attrs={'type':"text/javascript"}):
           row_data.append(row.text)
         img.append(re.findall("[^.]ttps.*jpg",row_data[2]))
    else:
         break
print("done loading chapters, now saving....")
for i,x in enumerate(img):
  if x==[]:
    img.remove([])
for i in range(len(img)):
      Image_URL=''.join(map(str,img[i]))
      response = requests.get(Image_URL,stream=True)
      if response.status_code == 200:  
          file = open("One_Punch_%d" % (i+1), 'wb')
          response.raw.decode_content = True
          shutil.copyfileobj(response.raw,file)
          del response
 