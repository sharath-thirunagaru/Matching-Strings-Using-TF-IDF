#This programs takes input reffile, srcfile, testline

import sys

import operator

import math

import time


def fileparser(filepath,testlines):
    f = open(filepath)
    titles=[]
    for i in range(testlines):
        line =f.readline()
        titles.append(line.split('|')[0])
    f.close()
    return titles

def tokenizer(iplist,reftitles):
    reftokenlist =[]
    reftokentfidf =[]

    for str in iplist:
        tokenlist =[]
        tfidflist =[]
        strsplitlist = str.lower().split()
        for token in strsplitlist:
            tokenlist.append(token)
            tf = float(strsplitlist.count(token))
            normtf = float(tf)/len(strsplitlist)
            tfidflist.append(calculatetfidf(token,normtf,reftitles))

        sumofsquares =0

        for tfidf in tfidflist:
            sumofsquares +=float(tfidf*tfidf)

        for i in range(len(tfidflist)):
            tfidflist[i]=float(tfidflist[i])/float(math.sqrt(sumofsquares))
        reftokenlist.append(tokenlist)
        reftokentfidf.append(tfidflist)
    
    return reftokenlist,reftokentfidf






def calculatetfidf(token,normtf,doclist):
    doccount = len(doclist)
    tokendoccount=0

    for doc in doclist:
        if token in doc.lower().split():
            tokendoccount +=1
    idf = float(math.log(float(doccount)/(1+tokendoccount)))

    return float(normtf)*idf


def match(reftitles,reftokenlist,reftokenidflist,srctitles,srctokenlist,srctokenidflist):
    srcindex=0
    

    srcmatchtfidf =[]
        
    for i in range(len(srctitles)):
        srctokens = srctokenlist[i]
        
        matchtfidf =[]
    
        for k in range(len(reftitles)):
            matchtfidf.append([])

        srctokenidx =0

        for token in srctokens:
            refindex=0
            for reftokens in reftokenlist:
                   try:
                       tokenmatchidx = reftokens.index(token)
                   except:
                       tokenmatchidx=None
                   if tokenmatchidx >= 0:
                       reftfidfs = reftokenidflist[refindex]
                       #print token, i,srctokenidx,'  ---  ',
                       matchtfidf[refindex].append(float(reftfidfs[tokenmatchidx])*srctokenidflist[i][srctokenidx])
                   refindex+=1
            srctokenidx+=1
        srcmatchtfidf.append(matchtfidf)

    return srcmatchtfidf
    



def main():
    #args = sys.argv
    #reffile =args[1]
    #sourcefile =args[2]
    #testlines = args[3]

    starttime = time.time()
    reffile =raw_input('Enter the reffile path')
    sourcefile =raw_input('Enter the srcfile path')
    reftestlines = input('Enter number of lines to readin ref data')
    testlines = input('Enter the number of test lines')

    print 'Ref file : ',reffile
    print 'Source file: ',sourcefile

    reftitles = fileparser(reffile,int(reftestlines))
    srctitles = fileparser(sourcefile,int(testlines))

    #srctitles =['0 TO 100  THE CATCH UP','ADOLESCENCE']
    #print reftitles
    #print srctitles

    r=tokenizer(reftitles,reftitles)
    reftokenlist =r[0]
    reftokenidflist =r[1]

    s = tokenizer(srctitles,reftitles)
    srctokenlist = s[0]
    srctokenidflist =s[1]
##    
##    print reftokenlist
##
##
##    print '*'*20
##    
##    print reftokenidflist
##
##    print '*'*20
##
##    print srctokenlist
##
##    print '*'*20
##
##    print srctokenidflist

    srcmatches = match(reftitles,reftokenlist,reftokenidflist,srctitles,srctokenlist,srctokenidflist)

    #print srcmatch[0]
    refsrcweight =[]
    for srcmatch in srcmatches:
        sumweight =[]
        for l in  srcmatch:
            sumweight.append(sum(l))
        refsrcweight.append(list(enumerate(sumweight)))

    #print refsrcweight

    finalsortedweights =[]
    for finalweight in refsrcweight:
        finalweight.sort(key =operator.itemgetter(1),reverse=True)

        finalsortedweights.append(finalweight)
    

    #print finalsortedweights

    threshold =0.6
    srindex=0
    
    matchesfound =0
    f= open('C:\Users\snagaru\MDI\EDGAR\MatchProcess\Datasets\matchoutput.txt','wb')
    for srctitle in srctitles:
        f.write( '------ '+srctitle+'  ------Matches --- Max score  :'+str(finalsortedweights[srindex][0][1])+ '\n')
        suggmatches=0
        for sortedweights in finalsortedweights[srindex]:
            if sortedweights[1]>threshold:
                suggmatches+=1
                f.write(reftitles[sortedweights[0]]+'\n')
        srindex+=1
        if suggmatches>0:
            matchesfound+=1
    f.close()

    print 'Finsihed matching ',testlines,' titles, Found Matches for ',matchesfound,' in ',time.time()-starttime
if __name__=='__main__':
    main()
