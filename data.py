#!/usr/bin/python
# -*- coding: utf-8 -*-
#author: Tianming Lu

from scipy import stats
import numpy as np
import random

def generate(D, T, I, L, N):
    #generate large itemsets
    correlation_level = 0.5
    large_sets = []
    size = 0
    for i in range(L):
        sz = stats.poisson.rvs(I)
        if sz == 0:
            sz += 1

        if i == 0:
            itemsets = random.sample(xrange(N), sz)
            itemsets.sort()
            large_sets.append(itemsets)
        else:
            pick_items_p = 2
            while pick_items_p > 1:
                pick_items_p = stats.expon.rvs(scale=correlation_level)
            pick_items_count = int(pick_items_p * sz)
            pick_items = random.sample(large_sets[-1], min(pick_items_count, size))
            random_items = random.sample([x for x in xrange(N) if x not in pick_items],
                                         sz - len(pick_items))
            itemset = pick_items + random_items
            itemset.sort()
            large_sets.append(itemset)

        size = sz
    sets_p = stats.expon.rvs(size = L)
    sets_p = np.array(sets_p)
    sump = sum(sets_p)
    sets_p /= sump

    corruption_levels = stats.norm.rvs(0.5, 0.1, size = L)
    trans = []
    tran_size = stats.poisson.rvs(T, size = D)
    for i in range(D):
        P = np.random.rand(L)
        P = sets_p * P
        index = np.argmax(P)
        itemset = list(large_sets[index])

        c = corruption_levels[index]
        set_size = len(itemset)
        while stats.uniform.rvs() < c and set_size > 1:
            index = stats.randint.rvs(0, set_size)
            itemset.pop(index)
            set_size -= 1
        trans.append(itemset)
    return trans

def write(transactions, filename):
    with open(filename, 'w') as output:
        for t in transactions:
            for item in t:
                output.write(str(item) + ' ')
            output.write('\n')

def read(filename):
    transactions = []
    with open(filename, 'r') as input:
        for line in input.readlines():
            t = [item for item in line.split()]
            transactions.append(t)
    return transactions

if __name__ == "__main__":
    trans = generate(10000, 20, 4, 2000, 1000)
    write(trans, "test.txt")
