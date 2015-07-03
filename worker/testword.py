#coding:utf-8
#author:leanse

def Words():
    f = file("testword", "r+")
    words = []
    
    while True:
        str_line = f.readline()
        if not str_line:
            break
        
        ws = str_line[0:-1].split(' ')
        words.extend(ws)
    return words
     

if __name__ == "__main__":
    words = Words()
    i = 0
    for w in words:
        print i, w
        i += 1