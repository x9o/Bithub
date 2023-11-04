import requests

enurl = "https://raw.githubusercontent.com/coffee-and-fun/google-profanity-words/main/data/en.txt"
cnurl = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/zh"
ruurl = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/ru"


response = requests.get(enurl)
responez = requests.get(cnurl)
responser = requests.get(ruurl)
en = response.text.strip().split("\n")
zh= responez.text.strip().split("\n")
ru = responser.text.strip().split("\n")
allat = en + zh + ru

