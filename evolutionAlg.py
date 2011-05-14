import random
import matplotlib.pyplot as plt
import Image, ImageDraw

from gene_functions import exclusive, violation

# Drawing Name Settings
scorePlotNum = 32               # part of the plot name, feel free to change
scoreComment = "yourComment"    # part of the plot name, feel free to change
colorimComment = "yourComment"  # part of the plot name, feel free to change

# Internal Settings
#keylist = generateGraph1(100,100,50,30,20) # srcKey set above
nGood = 60          # number of Good Keys
nImpersonated = 60  # number of Impersonated Keys
nMadeup = 60        # number of Madeup Keys (keys that don't claim to be Good keys' people)
nCertGood = 30      # max number of certificates a Good Key may sign
nCertBad = 20       # max number of certificates an Impersonated or Madeup Key may sign
totalKeys = nGood + nImpersonated + nMadeup

totalgens = 200     # number of generations after initial gen
scale = 10          # tweaks how strongly consistency is violated
genSize = 100       # number of babies per generation
pickNum = 5         # number of babies picked to be as parents (asexually)
produceNum = genSize/pickNum # number of babies produced per parent
cTrustscale = 20    # srcKey's children's trusts are higher. The number of times to duplicate source node's children, i.e. if the source node starts with 3 children (getting 3 points), it will duplicate it to appear to have 60 children (60 points). The point is so that the source's children's trust should outweigh other node's childrens. (Trust the source the most!)
gcTrustscale = 4    # srcKey's grandchildren's trusts are higher
mutationRate = 0.01 # rate of swithing 0 and 1
srcKey = 5

# Output Settings
printStep = totalgens/10 # print score per printStep geneartions

# Drawing Internals
booPlot = True
scoresPlotList = []     # to be plotted with plt
scorePlotName = "plots/" + str(scorePlotNum) + "_ScorePlot_" + scoreComment + ".png"

colorim = Image.new("RGB", (800, 600), (0,0,0,0)) # image of all the coloring changes
draw = ImageDraw.Draw(colorim)
colorimName = "plots/" + str(scorePlotNum) + "_Colors_" + colorimComment + ".png"
if (totalgens > 600) or (totalKeys > 800):
    booPlot = False
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" 
    print "!!!! No Plots because generation > 600 or totalKeys > 800 "
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" 

# GENSIZE MUST BE <= 600 to fit in the 600-pixel height of picture
cim_yIncrement = 600/totalgens  # this can have up to 0.5 precision
# TOTALKEYS MUST BE <= 800 to fit in the 800-pixel width of picture
cim_xIncrement = int(800/totalKeys)


#########################################################################

class Key:
    def __init__(self, keyNum, nameNum, color, children = []):
        self.keyNum = keyNum
        self.nameNum = nameNum
        self.color = color          # black is 0, white is 1
        self.children = children    # children's keyNums
    def __str__(self):
        return str(self.keyNum) + "\t" + str(self.nameNum) + "\t" + \
            str(self.color) + "\t" + \
            str(self.children)
    def __repr__(self):
        return self.__str__()

# returns a dictionary of name --> keyNum list with that name
def nameDict(keylist):
    nameDict = {}
    for k in keylist:
        if k.nameNum in nameDict:
            # if the key's has been seen already
            nameDict[k.nameNum].append(k.keyNum)
        else:
            # else create a new name --> keyNum entry
            nameDict[k.nameNum] = [k.keyNum]
    return nameDict

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

def generateGraph1(nGood,nImpersonated,nMadeup,nCertGood,nCertBad):
    #Perfect world, no good guy ever signs bad guy
    keylist = []
    for i in range(0,nGood):
        numChild = random.randint(1,nCertGood)
        lst = []
        while len(lst) < numChild:
            target = random.randint(0,nGood-1)
            if target != i and not (target in lst):
                lst.append(target)
        keyG = Key(i,i,0,lst)
        keylist.append(keyG)

    for i in range(nGood,nGood+nImpersonated):
        numChild = random.randint(1,nCertBad)
        lst = []
        while len(lst) < numChild:
            target = random.randint(0,nGood+nImpersonated+nMadeup-1)
            if target != i and not (target in lst):
                lst.append(target)
        keyF = Key(i,random.randint(0,nGood-1),0,lst)
        keylist.append(keyF)

    for i in range(nGood+nImpersonated,nGood+nImpersonated+nMadeup):
        numChild = random.randint(1,nCertBad)
        lst = []
        while len(lst) < numChild:
            target = random.randint(0,nGood+nImpersonated+nMadeup-1)
            if target != i and not (target in lst):
                lst.append(target)
        keyB = Key(i,i,0,lst)
        keylist.append(keyB)

    return keylist



if __name__ == '__main__':
    print "Begin PGP Trust Ranking"
    print "using the Evolutionary Algorithm (note: asexual reproduction!)"
    print "\nDetails of this run:"
    print "Number of Generations:\t" + str(totalgens)
    print "Generation Size:\t" + str(genSize)
    print "Per generation, number of trust assignments to produce progeny:\t" + str(pickNum)
    print "Number of preset Good Keys:\t\t" + str(nGood)
    print "Number of preset Impersonated Keys:\t" + str(nImpersonated)
    print "Number of preset Madeup Keys:\t\t" + str(nMadeup)

    print
    keylist = generateGraph1(nGood,nImpersonated,nMadeup,nCertGood,nCertBad) # srcKey set above

    # Increase trust for srckey's grandchildren and children
    for n in keylist[srcKey].children:
        keylist[n].children = keylist[n].children*gcTrustscale
    keylist[srcKey].children = keylist[srcKey].children*cTrustscale
    
    #print "Initial graph: "
    #for k in keylist: print k

    # Generation 0: randomly assign trust color 20 times
    # each time remembers: geneScore --> colorAssignments
    oldGen = {}
    newGen = {}
    print "===================================\n"
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

        # put the best score in the plot list
        scoresPlotList.append(scores[0])
        if booPlot:
            # draw a row of colors on colorImage
            bestColorAssignment = oldGen[scores[0]]
            for i in range(totalKeys): # == len(bestColorAssignment)
                upperleftX = i * cim_xIncrement 
                upperleftY = g * cim_yIncrement
                lowerightX = (i+1) * cim_xIncrement
                lowerightY = (g+1) * cim_yIncrement
                thefill = "white" if bestColorAssignment[i] == 1 else "black"
                draw.rectangle((upperleftX, upperleftY, lowerightX, lowerightY), fill=thefill)

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
                    #for k in keylist: print k
                    print "new geneScore = " + str(geneScore)

                newGen[geneScore] = newColorAssignments

        # resetting stuff
        oldGen = newGen
        newGen = {}

    # print out the best assignment's keylist
    # sort the scores (keys of oldGen dictionary)
    scores = oldGen.keys()
    scores.sort()
    # put the score in the plot list
    scoresPlotList.append(scores[0])
    # pick best one
    print "\nFINAL SCORE: " + str(scores[0])
    oldColorAssignment = oldGen[scores[0]]
    resetKeyColors(keylist, oldColorAssignment)
    # print "Final assignments:"
    # for k in keylist: print k

    if booPlot:
        # plot the scores
        plt.plot(scoresPlotList)
        plt.ylabel('Score (higher = worse)')
        plt.xlabel('Generation Numbers')
        plt.savefig(scorePlotName)

        # draw the colors
        colorim.save(colorimName)

        print
        print "See your plots at:"
        print "Score plot: " + scorePlotName
        print "Trust plot: " + colorimName
    else:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" 
        print "!!!! No Plots because generation > 600 or totalKeys > 800 "
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" 
