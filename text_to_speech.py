import os,time
def robot(text):
    os.system("espeak ' " + text + " ' --stdout |aplay")
    
#robot("I am dee")