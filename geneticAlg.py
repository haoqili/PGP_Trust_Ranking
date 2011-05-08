import random

from gene_functions import exclusive, violation
from simple_functions import nameDict
from weighted_test import generateGraph1

printStep = 200     # print score per printStep geneartions

scale = 10          # tweaks how strongly consistency is violated
totalgens = 1000    # number of generations after initial gen
genSize = 100       # number of babies per generation
pickNum = 5         # number of babies picked to be as parents (asexually)
produceNum = genSize/pickNum    # number of babies produced per parent
cTrustscale = 10    # srcKey's children's trusts are higher
gcTrustscale = 2    # srcKey's grandchildren's trusts are higher
mutationRate = 0.01 # rate of swithing 0 and 1
srcKey = 5

class Key:
    def __init__(self, keyNum, nameNum, color, parents = [], children = []):
        self.keyNum = keyNum
        self.nameNum = nameNum
        self.color = color          # black is 0, white is 1
        self.parents = parents      # parent's keyNums
        self.children = children    # children's keyNums
    def __str__(self):
        return str(self.keyNum) + "\t" + str(self.nameNum) + "\t" + \
            str(self.color) + "\t" + \
            str(self.parents) + "\t" + str(self.children)
    def __repr__(self):
        return self.__str__()

# the genetic algorithm:
# - randomly assigns trust worthiness number to each node
# - run functions to get the best assignments
def geneticAlg(s_keyNum, keylist): # source, keylist
    geneScore = 0 # LOWER means better
    
    # step 1. geneScore contribution from each name group
    # run names on gene_functions' exclusive(lst,scale):
    # Go through, find a list of names
    nameGroups = nameDict(keylist)
    #print "Names in graph/keylist:"
    #print nameGroups

    for namegroup in nameGroups:
        #print "namegroup: " + str(namegroup)
        # make a list of that name's color list
        nameColorList = []
        for key in nameGroups[namegroup]:
            nameColorList.append(keylist[key].color)
        #print "nameColorList: " + str(nameColorList)
        # call exclusive on nameColorList
        nameScore = exclusive(nameColorList, scale)
        geneScore += nameScore
        #print "nameScore:     " + str(nameScore)

    # step 2. geneScore contribution from each pair
    # violation := moreTrustworthy (higher #) --> lessTrustworthy (lower #)
    # iterate through pairs call gene_functions' violation on each
    for k in keylist:
        for child in k.children:
            #print "pair: " + str(k.keyNum) + " --> " + str(child)
            #print "colr: " + str(k.color) + " --> " + str(keylist[child].color)
            pairScore = violation(k.color, keylist[child].color)
            geneScore += pairScore
            #print "score\t " + str(pairScore)

    return geneScore

# randomize the trust-score (color) of each key
# except for src, which has full trust, i.e 1
# returns keyColor list
def randColors(keylist, srcKey):
    colorAssignments = []
    for key in keylist:
        if key.keyNum == srcKey:
            key.color = 1
        else:
            key.color = random.randint(0,1)
        colorAssignments.append(key.color)
    return colorAssignments

# from a sequence of oldColors list generate a color assisgnment 
# in the newGeneration w/ random mutations
# THE ORDER OF COLORS BETTER CORRESPOND TO KEY NUM
# returns keyColor list
def aBabysColors(oldColors, srcKey, genNum):
    aBabysColors = []
    # mutate each key's color based on random gaussian :D yay Python!!
    newColor = 0
    for j in range(len(oldColors)):
        if j == srcKey: # srcKey's color is always 1
            newColor = 1
        else:
            # switch colors with mutationRate probability
            color = oldColors[j]
            roll = random.uniform(0,1)
            if roll < mutationRate:
                if color == 1:
                    newColor = 0
                else:
                    newColor = 1
            else:
                newColor = color
        aBabysColors.append(newColor)
    return aBabysColors
        
# reset the colors of keylist
# THE ORDER OF COLORS BETTER CORRESPOND TO KEY NUM
def resetKeyColors(keylist, newColorAssignments):
    for i in range(len(newColorAssignments)):
        keylist[i].color = newColorAssignments[i]

if __name__ == '__main__':
    print "Begin PGP Trust Ranking"
    print "using the Genetic Algorithm"
    print "20 trust assignments for each generation, 5 best survive to contribute 4 in the next generation with small modifications (no mating)" 

    print
    # good, fake, bad, max number of signatures for good, max sigs for bad
    # fake = pretending to be someone else. bad = made up people 
    keylist = generateGraph1(100,100,50,30,20) # srcKey set above

    # Increase trust for srckey's grandchildren and children
    for n in keylist[srcKey].children:
        keylist[n].children = keylist[n].children*gcTrustscale
    keylist[srcKey].children = keylist[srcKey].children*cTrustscale
    
    print "Initial graph: "
    for k in keylist: print k

    # Generation 0: randomly assign trust color 20 times
    # each time remembers: geneScore --> colorAssignments
    oldGen = {}
    newGen = {}
    print "\n===================================\n"
    print "Generation 0 "
    for i in range(genSize):
        # 1. get generation 0's colors
        #print "\nTrial " + str(i)
        colorAssignments = randColors(keylist, srcKey)

        # 2. see the updated colors keylist
        #print "keys in the graph for generation 0:"
        #for k in keylist: print k

        # 3. score this new keylist
        geneScore = geneticAlg(srcKey, keylist)
        #print "\n Initial Score for generation 0 = " + str(geneScore)

        oldGen[geneScore] = colorAssignments

    for g in range(totalgens):
        #print "\n===================================\n"
        #print "Generation " + str(g+1)

        # sort the scores (keys of oldGen dictionary)
        scores = oldGen.keys()
        scores.sort()
        #print "old scores: " + str(scores)

        # pick the pickNum best ones
        for i in range(pickNum):
            oldColorAssignment = oldGen[scores[i]]
            #print "\nOld Score: " + str(scores[i]) 
            #print " and its Color Assignments: " + str(oldColorAssignment)
            # each makes produceNum "babies" with small modifications
            for j in range(produceNum):
                # get this baby's colors
                newColorAssignments = aBabysColors(oldColorAssignment, srcKey, g)
                
                # 2. update colors keylist
                resetKeyColors(keylist, newColorAssignments)
            
                # 3. score this new keylist
                geneScore = geneticAlg(srcKey, keylist)
                #print "keys in the graph:"
                if (g % printStep == 0) and (i ==0) and (j == 0):
                    print "\n g = " + str(g)
                    for k in keylist: print k
                    print "new geneScore = " + str(geneScore)

                newGen[geneScore] = newColorAssignments

        # resetting stuff
        oldGen = newGen
        newGen = {}

    # print out the best assignment's keylist
    # sort the scores (keys of oldGen dictionary)
    scores = oldGen.keys()
    scores.sort()
    # pick best one
    print "\nBEST SCORE: " + str(scores[0])
    oldColorAssignment = oldGen[scores[0]]
    resetKeyColors(keylist, oldColorAssignment)
    for k in keylist: print k
