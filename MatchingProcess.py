#This programs takes input reffile, srcfile, testline

import sys


def fileparser(filepath,testlines):
    f = open(filepath)
    titles=[]
    for i in range(testlines):
        line =f.readline()
        titles.append(line.split('|')[0])

    return titles

def tokenizer(iplist):

    tokenlist =[]
    for str in iplist:
        strsplitlist = str.lower().split()
        for token in strsplitlist:
            tokenlist.append(token)
            tf = strsplitlist.count(token)
            normtf = float(tf/len(strsplitlist))
            tfidf=calculatetfidf(token,normtf,iplist)






def calculatetfidf(token,normtf,doclist):
    doccount = len(doclist)
    tokendoccount=0

    for doc in doclist:
        if token in doc.lower().split():
            tokendoccount +=1
    idf = float(doccount/tokendoccount)

    return float(normtf*idf)






def main():
    args = sys.argv
    reffile =args[1]
    sourcefile =args[2]
    testlines = args[3]

    print 'Ref file : ',reffile
    print 'Source file: ',sourcefile

    reftitles = fileparser(reffile,int(testlines))
    srctitles = fileparser(sourcefile,int(testlines))

    print reftitles
    print srctitles





if __name__=='__main__':
    main()
