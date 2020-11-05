import re
from bs4 import BeautifulSoup
import requests
import shutil,os
img=[]
name=""
chapter=""
end_chapter=""
mangapandalink = "http://www.mangapanda.com"

def menu():
  menu = {}
  menu['1']= "View current Popular manga titles" 
  menu['2']= "Download single manga title"
  menu['3']= "Download multiple chapters of manga title"
  menu['4']= "View current manga being tracked"
  menu['5']= "Track new Manga"
  menu['6']= "Download tracked manga if title has updated"
  menu['7']= "Exit"
  while True: 
    options=menu.keys()
    options.sort()
    print("Menu: ")
    for entry in options: 
      print entry, menu[entry]

    selection=raw_input("Please Select option number:") 
    if selection =='1': 
      printPopularList() 
    elif selection == '2': 
      runSingleMangaDownloadRoutine()
    elif selection == '3': 
      runMultipleMangaDownloadRoutine()       
    elif selection == '4': 
      print "Not yet implemented"
    elif selection == '5': 
      print "Not yet implemented"
    elif selection == '6': 
      print "Not yet implemented"
    elif selection == '7': 
      print "GoodBye!!"
      break
    else: 
      print "Unknown Option Selected!"

def runSingleMangaDownloadRoutine():
  global name 
  name = raw_input("Enter manga name: ")
  # remove spaces in name
  name= name.replace(' ', '-').lower()
  global chapter
  chapter =raw_input("Enter chapter number: ")
  chapter=int(chapter)

  print("\nRunning...\n")

  global mangadestinationDir
  mangadestinationDir =name+' '+str(chapter)
  if not os.path.exists(mangadestinationDir): 
  				os.makedirs(mangadestinationDir)

  download_page(mangapandalink)
  save_chapters()

def runMultipleMangaDownloadRoutine():
  global name 
  name = raw_input("Enter manga name: ")
  # remove spaces in name
  name= name.replace(' ', '-').lower()
  global chapter
  global end_chapter
  global mangadestinationDir
  chapter =raw_input("Enter first chapter number: ")
  chapter=int(chapter)
  chapteritr = chapter
  end_chapter =raw_input("Enter last chapter number: ")
  end_chapter=int(end_chapter)
  # increase to make range inclusive
  end_chapter = end_chapter+1
  print("\nRunning...\n")

  for chap in range(chapteritr,end_chapter):
    mangadestinationDir =name+' '+str(chap)
    chapter = chap
    if not os.path.exists(mangadestinationDir): 
            os.makedirs(mangadestinationDir)
    download_page(mangapandalink)
    save_chapters() 

def printPopularList():
  URL = mangapandalink
  request = requests.get(URL)
  if request.status_code == 200:
      page = requests.get(URL)
      page_content = BeautifulSoup(page.content,'html.parser')   
      popularmanga=[] 
      print("Here's a list of the current most popular manga ")
      #  get popular manga links and add their text to array
      for popularitemcaption in page_content.findAll('a', attrs={'class':"popularitemcaption"}):
        print "- {}".format(popularitemcaption.string)        
        popularmanga.append(popularitemcaption.string)               
  else:
      print("Error retreiving manga list")
        
def download_page(link):  
  for j in range(1,200):
    URL = "http://www.mangapanda.com/{}/{}/{}".format(name,chapter,j)
    print(URL)
    request = requests.get(URL)
    if request.status_code == 200:
          page = requests.get(URL)
          page_content = BeautifulSoup(page.content,'html.parser')         
          row_data=[]
          for row in page_content.findAll('script',attrs={'type':"text/javascript"}):          
            row_data.append(row.string)            
          img.append(re.findall("[^.]ttps.*jpg",row_data[2]))      
    else:
          break
  print("successfuly loaded chapter, now saving....")

def save_chapters():
  for i,x in enumerate(img):
    if x==[]:
      img.remove([])
  for i in range(len(img)):
        Image_URL=''.join(map(str,img[i]))
        response = requests.get(Image_URL,stream=True)
        if response.status_code == 200:  
            file_name = "{}/{}{}".format(mangadestinationDir,name,i+1)
            file = open(file_name, 'wb')
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw,file)
            del response

menu()






 