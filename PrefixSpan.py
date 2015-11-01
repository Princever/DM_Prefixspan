#coding=utf-8
__author__ = 'Prince'

import sys
import util as u



PLACE_HOLDER = '_'

class SquencePattern:
    def __init__(self, squence, support):
        self.squence = []
        for s in squence:
            self.squence.append(list(s))
        self.support = support

    def append(self, p):
        if p.squence[0][0] == PLACE_HOLDER:
            first_e = p.squence[0]
            first_e.remove(PLACE_HOLDER)
            self.squence[-1].extend(first_e)
            self.squence.extend(p.squence[1:])
        else:
            self.squence.extend(p.squence)
        self.support = min(self.support, p.support)


def prefixSpan(pattern, S, threshold):
    patterns = []
    f_list = frequent_items(S, pattern, threshold)

    for i in f_list:
        p = SquencePattern(pattern.squence, pattern.support)
        p.append(i)
        patterns.append(p)

        p_S = build_projected_database(S, p)
        p_patterns = prefixSpan(p, p_S, threshold)
        patterns.extend(p_patterns)

    return patterns


def frequent_items(S, pattern, threshold):
    items = {}
    _items = {}
    f_list = []
    if S is None or len(S) == 0:
        return []

    if len(pattern.squence) != 0:
        last_e = pattern.squence[-1]
    else:
        last_e = []
    for s in S:

        #class 1
        is_prefix = True
        for item in last_e:
            if item not in s[0]:
                is_prefix = False
                break
        if is_prefix and len(last_e) > 0:
            index = s[0].index(last_e[-1])
            if index < len(s[0]) - 1:
                for item in s[0][index + 1:]:
                    if item in _items:
                        _items[item] += 1
                    else:
                        _items[item] = 1

        #class 2
        if PLACE_HOLDER in s[0]:
            for item in s[0][1:]:
                if item in _items:
                    _items[item] += 1
                else:
                    _items[item] = 1
            s = s[1:]

        #class 3
        counted = []
        for element in s:
            for item in element:
                if item not in counted:
                    counted.append(item)
                    if item in items:
                        items[item] += 1
                    else:
                        items[item] = 1

    f_list.extend([SquencePattern([[PLACE_HOLDER, k]], v)
                   for k, v in _items.iteritems()
                   if v >= threshold])
    f_list.extend([SquencePattern([[k]], v)
                   for k, v in items.iteritems()
                   if v >= threshold])
    sorted_list = sorted(f_list, key=lambda p: p.support)
    return sorted_list


def build_projected_database(S, pattern):
    """
    suppose S is projected database base on pattern's prefix,
    so we only need to use the last element in pattern to
    build projected database
    """
    p_S = []
    last_e = pattern.squence[-1]
    last_item = last_e[-1]
    for s in S:
        p_s = []
        for element in s:
            is_prefix = False
            if PLACE_HOLDER in element:
                if last_item in element and len(pattern.squence[-1]) > 1:
                    is_prefix = True
            else:
                is_prefix = True
                for item in last_e:
                    if item not in element:
                        is_prefix = False
                        break

            if is_prefix:
                e_index = s.index(element)
                i_index = element.index(last_item)
                if i_index == len(element) - 1:
                    p_s = s[e_index + 1:]
                else:
                    p_s = s[e_index:]
                    index = element.index(last_item)
                    e = element[i_index:]
                    e[0] = PLACE_HOLDER
                    p_s[0] = e
                break
        if len(p_s) != 0:
            p_S.append(p_s)

    return p_S


def print_patterns(patterns):
    for p in patterns:
        name = '['
        for each in p.squence:
            aitem = '['
            flag = False
            for item in each:
                if flag:
                    aitem += '&'
                aitem += item
                flag = True
            aitem += ']'
            name += aitem
            name += ']'
        print("pattern:{0}, support:{1}".format(name, p.support))
        print >> ff,("pattern:{0}, support:{1}".format(name, p.support))



if __name__ == "__main__":
    ff = open('datas/result.txt','w')
    S = u.read("datas/gxyseq.csv")
    min_supp=0.01
    count = 0
    for each in S:
        count += 1
    patterns = prefixSpan(SquencePattern([], sys.maxint), S, min_supp * count)
    print_patterns(patterns)
    seqNums = []
    for each in patterns:
        seqNums.append(each.squence)
    maxSeqs = u.maxSeq(seqNums)
    print("The sequential patterns :")
    for i in maxSeqs:
        for sth in i:
            print "[",
            for ssth in sth:
                print ssth,
            print "]",
        print ""
    print >> ff,"The sequential patterns :"
    for i in maxSeqs:
        for sth in i:
            print >> ff,"[",
            for ssth in sth:
                print >> ff,ssth,
            print >> ff,"]",
        print >> ff,""
    ff.close()
    flitedSeqs = u.fliter(maxSeqs)
    expandedSeqs = u.expand(maxSeqs)
    maxStages = u.genPlotDatas(maxSeqs)
    flitedStages = u.genPlotDatas(flitedSeqs)
    expandedStages = u.genPlotDatas(expandedSeqs)
    allStages = []
    allStages += [maxStages]
    allStages += [flitedStages]
    allStages += [expandedStages]
    u.drawStages(allStages)
