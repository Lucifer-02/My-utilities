import clipboard
import sys
from termcolor import colored
import datetime
import platform

# get content in clipboard
content = clipboard.paste().replace("\n", "").replace('\r', '').replace('\t', '')

print("------------------------------------------------------------")
print(content)
print("------------------------------------------------------------")

# check my respond, count letter and save data
gess = 0
answer = 0 
path = ""
if platform.system() == "Linux":
    path = "/run/media/lucifer/STORAGE/IMPORTANTS/CODE/my_tools/count_word_data.txt"
else:
    path = "D:/IMPORTANTS/CODE/my_tools/count_word_data.txt"
    
file = open(path, "a")
for arg in sys.argv[1:]:
    gess = input("what u gess number of \""+ arg + "\"? ")
    answer = content.count(arg) 
    print(colored(str(arg), 'red', 'on_white') + " is: " + colored(str(answer), 'yellow'))
    file.write(str(datetime.datetime.now()) + ";" + content + ";" + arg + ";" +  str(gess) + ";" + str(answer) + "\n")

file.close()
