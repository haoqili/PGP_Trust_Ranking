class Key:
    def __init__(self, keyNum, nameNum, color, parents = [], children = []):
        self.keyNum = keyNum
        self.nameNum = nameNum
        self.color = color          # black is 0, white is 1
        self.parents = parents      # parent's keyNums
        self.children = children    # children's keyNums
    def __str__(self):
        return str(self.keyNum) + "\t" + str(self.nameNum) + "\t" + \
            str(self.parents) + "\t" + str(self.children)
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

# count the number of violations there are in the graph/keyList
# violation := white (1) --> black (0)
def countViolations(keylist):
    count = 0
    # iterate through all the white nodes
    for k in keylist:
        if k.color == 1:
            # add one for each black children
            for child in k.children:
                if keylist[child].color == 0:
                    count += 1
    return count

# Go through all possible color ( 1 or 0) that is
# consistent with "There Should Be One Real John"
# weight each assignment by how many there are and
# Calculate trustworthyness of each node
# TSBORJ = either all Johns are untrusted, or 1 trust others untrusted
def weightedAlg(s_keyNum, keylist):
    n = len(keylist)
    Trust = {}
    for stuff in keylist:
        Trust[stuff.keyNum] = 0

    
    nameGroup = nameDict(keylist)
    names = nameGroup.keys()
    
    lenlst = [len(nameGroup[i])+1 for i in nameGroup]

    totalPerm = 1
    for i in lenlst:
        totalPerm = totalPerm*i

    totalWeight = 0

    for i in range(totalPerm):
        assignment = {}
        
        for j in range(len(lenlst)):
            mod = lenlst[-j-1]
            value = i % mod
            i = (i - value)/mod
            assignment[names[-j-1]] = value

        for j in keylist:
            j.color = 0
        
        for j in assignment:
            if assignment[j] != 0:
                keylist[nameGroup[j][assignment[j]-1]].color = 1
        keylist[s_keyNum].color = 1

        #print [(k.keyNum,k.color) for k in keylist]
        ###### end of color assignment ####

        violations = countViolations(keylist)
        
        curWeight = 2**(-4*violations)
        totalWeight = totalWeight + curWeight

        for j in keylist:
            Trust[j.keyNum] = Trust[j.keyNum] + j.color*curWeight

    for node in Trust:
        Trust[node] = float(Trust[node]/totalWeight)
        

    print Trust
        

if __name__ == '__main__':
    print "Begin PGP Trust Ranking"
    print "using the Weighted Algorithm"
    
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


    weightedAlg(5,keylist)
