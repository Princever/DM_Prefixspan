#coding=utf-8
__author__ = 'Prince'

import copy
import csv
import numpy as np
import pylab as pl
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getItems(seqs):
    items = []
    for custom in seqs:
        for basket in custom:
            for item in basket:
                if [item] not in items:
                    items.append([item])
                    
    items.sort()
    return items

def getMapNum(item,transmap):
    for k in transmap.keys():
        if [item] == transmap[k]:
            return k
        else:
            pass
    return 0

def getMapSeq(items,seqs):
    transmap = {}
    value = 1
    for each in items:
        transmap[value]=each
        value += 1

    mapSeq = []
    tmpbasket = []
    tmpcustom = []
    for custom in seqs:
        for basket in custom:
            for item in basket:
                tmpbasket += [getMapNum(item,transmap)]
            tmpcustom.append(tmpbasket)
            tmpbasket = []
        mapSeq.append(tmpcustom)
        tmpcustom =[]
    return mapSeq

def mapBack(resultSeq,transmap):
    FinalSeq = []
    tmpbasket = []
    tmpcustom = []
    for custom in resultSeq:
        for basket in custom:
            for item in basket:
                tmpbasket += transmap[item]
            tmpcustom.append(tmpbasket)
            tmpbasket = []
        FinalSeq.append(tmpcustom)
        tmpcustom =[]

    return FinalSeq

def getTransmap(items):
    transmap = {}
    value = 1
    for each in items:
        transmap[value]=each
        value += 1

    return transmap

def isInSeq(nseq,tseq):
    result = []
    cp = 0
    np = 0
    count = 0
    for each in tseq:
        count += 1

    pos = 0
    for each in nseq:
        result.append(False)
        pos += 1

    npos = -1
    for nbasket in nseq:
        npos += 1
        if np == count:
            # print "npos:",npos,"pos:",pos
            break
        nbset = set(nbasket)
        # print "nbset:",nbset
        np = 0
        for tbasket in tseq:
            if np < cp:
                np += 1
                # print "np:",np,"cp:",cp,",pass"
                pass
            else:
                tbset = set(tbasket)
                # print "tbset:",tbset
                np += 1
                if tbset.issuperset(nbset):
                    # print "find:nbset:",nbset,"tbset:",tbset
                    result[npos] = True
                    cp = np
                    # print "np:",np,"cp:",cp
                    break
                else:
                    result[npos] = False
                    # print "np:",np,"count:",count
                
    outcome = True  
    for each in result:
        outcome &= each
    return outcome



def maxSeq(seqs):
    maxSeq = copy.deepcopy(seqs)
    items = getItems(maxSeq)
    transmap = getTransmap(items)
    mapSeq = getMapSeq(items,maxSeq)
    resultSeq = copy.deepcopy(mapSeq)

    npos = 0
    for nseq in mapSeq:
        npos += 1
        tpos = 0
        for tseq in mapSeq:
            tpos += 1
            if npos == tpos:
                pass
            else:
                if isInSeq(nseq,tseq):
                    # print "npos:",npos,"tpos:",tpos
                    # print "nseq:",nseq,"tseq:",tseq,"removed"
                    resultSeq.remove(nseq)
                    break

    FinalSeq = mapBack(resultSeq,transmap)

    return FinalSeq

def read(filename):
    csvfilein = file(filename,'rb')
    reader = csv.reader(csvfilein)
    baskets=[]
    customs=[]
    for line in reader:
        for term in line:
            item = term.split(',')
            items = []
            for sth in item:
                items.append(sth)    
            baskets.append(item)   
        customs.append(baskets)
        baskets=[]
    return customs

def genStage(maxSeqs):
    allitem = getItems(maxSeqs)
    allitems = []
    for each in allitem:
        allitems += each
    items = {}
    for each in allitems:
        items.setdefault(each,0)
    return items

def genPlotDatas(maxSeqs):
    stages = []
    count = 0
    while count <10:
        stages.append({})
        stages[count] = genStage(maxSeqs)
        count += 1
    for custom in maxSeqs:
        nowstage = 0
        for basket in custom:
            for item in basket:
                stages[nowstage][item] += 1
            nowstage += 1
            if nowstage >= 10:
                break

    return stages

def figureStage(index, stages):
    stagex = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pl.figure(index)
    stageys = {}
    items = []
    for each in stages[0].keys():
        items += [each]

    for eachitem in items:
        stageys[eachitem] = []
        for eachstage in stages:
            stageys[eachitem] += [eachstage[eachitem]]

    # print stageys

    for eachy in stageys.keys():
        # print eachy
        pl.plot(stagex, stageys[eachy], label = eachy)# use pylab to plot x and y
        pl.plot(stagex, stageys[eachy], 'o')

    pl.legend(loc= 'best', numpoints=1, fontsize = 5,handletextpad = 1, ncol = 2)

def drawStages(allStages):
    count = 1
    for each in allStages:
        figureStage(count, each)
        count += 1
    
    # items = []
    # for each in maxStages[0].keys():
    #     items += [each]

    # for eachitem in items:
    #     stageys[eachitem] = []
    #     for eachstage in maxStages:
    #         stageys[eachitem] += [eachstage[eachitem]]

    # for eachy in stageys.keys():
    #     # print eachy
    #     pl.plot(stagex, stageys[eachy], label = eachy)# use pylab to plot x and y
    #     pl.plot(stagex, stageys[eachy], 'o')

    # pl.legend(loc= 'best', numpoints=1, fontsize = 7,handletextpad = 1)

    # pl.figure(2)

    # items = []
    # for each in flitedStages[0].keys():
    #     items += [each]

    # for eachitem in items:
    #     stageys[eachitem] = []
    #     for eachstage in flitedStages:
    #         stageys[eachitem] += [eachstage[eachitem]]

    # for eachy in stageys.keys():
    #     # print eachy
    #     pl.plot(stagex, stageys[eachy], label = eachy)# use pylab to plot x and y
    #     pl.plot(stagex, stageys[eachy], 'o')

    # pl.legend(loc= 'best', numpoints=1, fontsize = 7,handletextpad = 1)


    # leg = pl.gca().get_legend()
    # ltext  = leg.get_texts()
    # pl.setp(ltext, fontsize='small')
    pl.show()# show the plot on the screen

def fliter(maxSeqs):
    result = []
    for each in maxSeqs:
        count = 0
        for one in each:
            count += 1
        if count >= 2:
            result.append(each)

    # print result
    return result

def expand(maxSeqs):
    result = []
    for each in maxSeqs:
        tmp = []
        count = 0
        for one in each:
            count += 1
        time1 = 0
        
        if count == 2:   
            while time1 <= 1:
                time2 = 0
                while time2 <= 4:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count == 3:
            while time1 <= 2:
                time2 = 0
                while time2 <= 2:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count == 4:
            while time1 <= 3:
                time2 = 0
                while time2 <= 1:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count == 5:
            while time1 <= 4:
                time2 = 0
                while time2 <= 1:
                    tmp.append(each[time1])
                    time2 += 1
                time1 += 1
        if count >= 6:
            tmp += each

        if tmp != []:
            result += [tmp]
    return result






























