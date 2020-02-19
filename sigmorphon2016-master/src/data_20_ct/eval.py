#!/usr/bin/env python
"""
Official Evaluation Script for the SIGMORPHON 2016 Shared Task.

Returns accuracy, mean Levenhstein distance and mean reciprocal rank.

Author: Ryan Cotterell and Mans Hulden
Last Update: 12/01/2015
"""

import sys
import numpy as np
import codecs
from collections import defaultdict as dd


def distance(str1, str2):
    """Simple Levenshtein implementation for evalm."""
    m = np.zeros([len(str2)+1, len(str1)+1])
    for x in range(1, len(str2) + 1):
        m[x][0] = m[x-1][0] + 1
    for y in range(1, len(str1) + 1):
        m[0][y] = m[0][y-1] + 1
    for x in range(1, len(str2) + 1):
        for y in range(1, len(str1) + 1):
            if str1[y-1] == str2[x-1]:
                dg = 0
            else:
                dg = 1
            m[x][y] = min(m[x-1][y] + 1, m[x][y-1] + 1, m[x-1][y-1] + dg)
    return int(m[len(str2)][len(str1)])


def evaluate(gold, guess):
    " Evaluates a single tag "

    # best guess
    best = guess
    # compute the metrics
    acc = 1.0 if best == gold else 0
    # edit distance
    lev = distance(best, gold)

    return float(acc), float(lev)    

if __name__ == "__main__":

    filenamesTwenty = ['subject1.txt', 'subject2.txt']
    results = open('stats.txt', 'w')


    meanAccuracy = 0
    meanLevDist = 0

    for file in filenamesTwenty:

        guesses = []
        gold = []
        meanAccuracySingle = 0
        meanLevDistSingle = 0
        
        data = open(file)

        for line in data:
            words = line.split()
            guesses.append(words[0])
            gold.append(words[1])

        for guess in guesses:
            
            eval = evaluate(guess, gold[guesses.index(guess)])
            meanAccuracySingle += eval[0]
            meanLevDistSingle += eval[1]

            print(eval)

        meanAccuracySingle /= len(guesses)
        meanLevDistSingle /= len(guesses)

        results.write("\nSubject " + str(filenamesTwenty.index(file)) + "\n")
        results.write("Mean Accuracy: " + str(meanAccuracySingle) + "\n")
        results.write("Mean Levenhstein Distance " + str(meanLevDistSingle) + "\n")

        meanAccuracy += meanAccuracySingle
        meanLevDist += meanLevDistSingle

    meanAccuracy /= len(filenamesTwenty)
    meanLevDist /= len(filenamesTwenty)

    print("Mean Accuracy:", meanAccuracy)
    print("Mean Levenhstein Distance", meanLevDist)

    results.write("-----------------------------------------------------")
    results.write("\nNet Mean Accuracy: " + str(meanAccuracy))
    results.write("\nNet Levenhstein Distance " + str(meanLevDist))