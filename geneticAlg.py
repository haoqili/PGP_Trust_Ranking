import random

from gene_functions import exclusive, violation
from simple_functions import nameDict

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
        scale = 2
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
            key.color = 1.0
        else:
            key.color = random.uniform(0,1) # float [0,1]
        colorAssignments.append(key.color)
    return colorAssignments

# from a sequence of oldColors list generate a color assisgnment 
# in the newGeneration w/ random mutations
# THE ORDER OF COLORS BETTER CORRESPOND TO KEY NUM
# returns keyColor list
def aBabysColors(oldColors, srcKey):
    aBabysColors = []
    # mutate each key's color based on random gaussian :D yay Python!!
    for j in range(len(oldColors)):
        if j == srcKey: # srcKey's color is always 1
            newColor = 1.0
        else:
            color = oldColors[j]
            mutation = random.gauss(0, 0.03)
            newColor = color + mutation
            if newColor > 1: newColor = 1
            if newColor < 0: newColor = 0
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

    # manually create a pgp map to test out the simplest algorithm
    # this initial graph has no conflicts
    keylist = [ Key(0, 4, 0, [], [1, 4]),
                Key(1, 1, 1, [0], [2, 3]),
                Key(2, 5, 1, [1], []),
                Key(3, 1, 0, [1, 4], [6]),
                Key(4, 2, 1, [0, 5], [3]),
                Key(5, 25, 0,  [], [4]),
                Key(6, 3, 0, [3], [])
           ]
    srcKey = 5

    # Generation 0: randomly assign trust color 20 times
    # each time remembers: geneScore --> colorAssignments
    oldGen = {}
    newGen = {}
    print "\n===================================\n"
    print "Generation 0 "
    for i in range(20):
        # 1. get generation 0's colors
        #print "\nTrial " + str(i)
        colorAssignments = randColors(keylist, srcKey)

        # 2. see the updated colors keylist
        #print "keys in the graph:"
        #for k in keylist: print k

        # 3. score this new keylist
        geneScore = geneticAlg(srcKey, keylist)
        print "geneScore = " + str(geneScore)

        oldGen[geneScore] = colorAssignments

    generations = 100 # x more generations after initial gen
    for g in range(generations):
        print "\n===================================\n"
        print "Generation " + str(g+1)

        # sort the scores (keys of oldGen dictionary)
        scores = oldGen.keys()
        scores.sort()
        print "old scores: " + str(scores)

        # pick the 5 best ones
        for i in range(5):
            oldColorAssignment = oldGen[scores[i]]
            print "\nOld Score: " + str(scores[i]) 
            #print " and its Color Assignments: " + str(oldColorAssignment)
            # each makes n "babies" with small modifications
            n = 4
            for j in range(n):
                # get this baby's colors
                newColorAssignments = aBabysColors(oldColorAssignment, srcKey)
                
                # 2. update colors keylist
                resetKeyColors(keylist, newColorAssignments)
                #print "keys in the graph:"
                #for k in keylist: print k
            
                # 3. score this new keylist
                geneScore = geneticAlg(srcKey, keylist)
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
    print "\n\nBEST SCORE: " + str(scores[0])
    oldColorAssignment = oldGen[scores[0]]
    resetKeyColors(keylist, oldColorAssignment)
    for k in keylist: print k
