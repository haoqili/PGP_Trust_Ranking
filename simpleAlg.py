class Key:
    def __init__(self, keyNum, nameNum, parents = [], children = []):
        self.keyNum = keyNum
        self.nameNum = nameNum
        self.parents = parents
        self.children = children
    def __str__(self):
        return str(self.keyNum) + "\t" + str(self.nameNum) + "\t" + \
            str(self.parents) + "\t" + str(self.children)
    def __repr__(self):
        return self.__str__()

# function to mark all descendants of src trustworthy
# return a list of trustworthy nodes' keyNums (i.e. descendats of src)
def markTrust(s_keyNum, keylist, trusted_nodes):
    # "mark" as trusted
    trusted_nodes.append(s_keyNum)

    #children is empty! return trusted nodes
    if not keylist[s_keyNum].children: 
        return trusted_nodes
    # recurse on children
    else:
        for child in keylist[s_keyNum].children:
            return markTrust(child, keylist, trusted_nodes)

# function to find first set of untrustworthy nodes
# = non-trustworthy nodes with same name as trustworthy
# return a list of untrustworthy nodes' keyNums
def markInitialUntrust(trustworthy, keylist):
    # get all the names of trustworthy nodes
    trustedNames = []
    for trustkeyNum in trustworthy:
        trustedNames.append(keylist[trustkeyNum].nameNum)

    # now go through all non-trustworthy nodes and see if name match
    untrustworthy = []
    for k in keylist:
        if k.keyNum not in trustworthy:
            if k.nameNum in trustedNames:
                untrustworthy.append(k.keyNum)
    return untrustworthy

def markAncestorsUntrust_helper(s_keyNum, keylist, untrusted_ancestors):
    # not marked here because the initial s_keyNum is not a parent, but an initial untrustworthy node

    #parents is empty! return trusted nodes
    if not keylist[s_keyNum].parents: 
        return untrusted_ancestors
    # recurse on parent
    else:
        for parent in keylist[s_keyNum].parents:
            # "mark" as untrusted
            untrusted_ancestors.append(parent)
            return markAncestorsUntrust_helper(parent, keylist, untrusted_ancestors)
# function to mark all ancestors of untrusted nodes, unstrusted too
# return a list of ancestors of unstrusted nodes (repeats possible)
def markAncestorsUntrust(untrustworthy, keylist):
    untrusted_ancestors = []
    for untrustedKeyNum in untrustworthy:
        untrusted_ancestors.extend( markAncestorsUntrust_helper(untrustedKeyNum, keylist, []) )
    return untrusted_ancestors

# the simple algorithm marks:
# - all descendants of source key trustworthy
# - pretenders of trustworthy keys untrustworthy
# - all ancestors of untrustworthy nodes untrustworthy
def simpleAlg(s_keyNum, keylist):
    print "in simpleAlg"
    
    src = keylist[s_keyNum]

    # step 1. find all trustworthy nodes
    # trustworthy nodes are direct descendants of src
    trustworthy = markTrust(s_keyNum, keylist, [])
    print "trustworthy nodes:"
    print trustworthy

    # step 2. Go through all the nodes, mark untrustworthy nodes
    # = nodes with same name as a trustworthy node (that are not trustworthy)
    untrustworthy = markInitialUntrust(trustworthy, keylist)
    print "untrustworthy nodes, initially:"
    print untrustworthy

    # step 3. recursively mark the ancestors of untrustworthy, untrustworthy too
    untrustworthy.extend( markAncestorsUntrust(untrustworthy, keylist) )
    print "untrustworthy nodes, after marked ancestors too:"
    print untrustworthy

    # go through keylist, if keyNum is neither trustworthy or untrustworthy, mark unsure
    unsure = []
    for k in keylist:
        if k.keyNum not in trustworthy:
            if k.keyNum not in untrustworthy:
                unsure.append(k.keyNum)
    print "unsure nodes:"
    print unsure

if __name__ == '__main__':
    print "Begin PGP Trust Ranking"

    # manually create a pgp map to test out the simplest algorithm
    # this initial graph has no conflicts
    keylist = [ Key(0, 4, [], [1, 4]),
                Key(1, 1, [0], [2, 3]),
                Key(2, 5, [1], []),
                Key(3, 1, [1, 4], [6]),
                Key(4, 2, [0, 5], [3]),
                Key(5, 25, [], [4]),
                Key(6, 3, [3], [])
           ]
    print "keys in the graph:"
    for k in keylist: print k

    simpleAlg(5, keylist)
