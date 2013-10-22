import requests, re

def RipSoundcloud(url):
  request = requests.get(url)
  streamurl_regex = '"streamUrl":"([^"]+)"'
  streamurl = re.search(streamurl_regex,request.text).group(1)
  title_regex = '"title":"([^"]+)"'
  title = re.search(title_regex,request.text).group(1)
  f = open(title + ".mp3","w")
  request = requests.get(streamurl)
  f.write(request.content)
  f.close()