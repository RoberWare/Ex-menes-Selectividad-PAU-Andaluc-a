# -*- coding: utf-8 -*-

import requests,os,sys,urllib

ruta = os.getcwd()

download_finished=False
progress=""
file_name=""

def progress_bar(link,*largs):
    global download_finished
    global progress
    global file_name
    n=0
    for x in link[::-1]:
        if x == "/":break
        else:n+=1
    print link[-n:]
    file_name = "./tmp/"+link[-n:]
    with open(file_name, "wb") as f:
            print "Downloading %s" % file_name
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')
    
            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    progress="\r[%s%s]" % ('=' * done, ' ' * (50-done)) 
                    sys.stdout.write(progress)    
                    sys.stdout.flush()
    download_finished=True
    print "\n",file_name,download_finished
    return False
    
def simplefile(link,name,*largs):
    testfile = urllib.URLopener()
    testfile.retrieve(link, name)