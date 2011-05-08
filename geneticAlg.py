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
    print "in geneticAlg"
    geneScore = 0 # LOWER means better
    
    # step 1. geneScore contribution from each name group
    # run names on gene_functions' exclusive(lst,scale):
    # Go through, find a list of names
    nameGroups = nameDict(keylist)
    print "Names in graph/keylist:"
    print nameGroups

    for namegroup in nameGroups:
        print "namegroup: " + str(namegroup)
        # make a list of that name's color list
        nameColorList = []
        for key in nameGroups[namegroup]:
            nameColorList.append(keylist[key].color)
        print "nameColorList: " + str(nameColorList)
        # call exclusive on nameColorList
        scale = 2
        nameScore = exclusive(nameColorList, scale)
        geneScore += nameScore
        print "nameScore:     " + str(nameScore)

    # step 2. geneScore contribution from each pair
    # violation := moreTrustworthy (higher #) --> lessTrustworthy (lower #)
    # iterate through pairs call gene_functions' violation on each
    for k in keylist:
        for child in k.children:
            print "pair: " + str(k.keyNum) + " --> " + str(child)
            print "colr: " + str(k.color) + " --> " + str(keylist[child].color)
            pairScore = violation(k.color, keylist[child].color)
            geneScore += pairScore
            print "score\t " + str(pairScore)

    print "geneScore = " + str(geneScore)

if __name__ == '__main__':
    print "Begin PGP Trust Ranking"

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
    print "keys in the graph:"
    for k in keylist: print k

    geneticAlg(5, keylist)
