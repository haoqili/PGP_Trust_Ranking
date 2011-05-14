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
