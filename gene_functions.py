import math

# scoring name group
def exclusive(lst,scale):
    n = len(lst)
    s = sum(lst)
    avg = float(s)/float(n)
    m = max(lst)
    if n == 1: #if theres only 1 guy in the group, no need to score for exclusivity
       return 0
    prod = 1
    lst.remove(m)
    for i in lst:
       prod = prod*(1-math.sqrt(i))
    return float(scale*prod**(1.0/(n-1)))

# scoring signs
def violation(aTrustScore,bTrustScore): #A signs B's public key
    if aTrustScore > bTrustScore:
       return float(aTrustScore - bTrustScore)
    return 0

'''
if __name__ == '__main__':
    lst1 = [0.67]
    lst2 = [0,0,0,1,0,0,0]
    lst3 = [0.5,0.5]
    lst4 = [0,0,0.1,0.1,0.2,0.9]
    lst5 = [0.9,0.1,0,0,0]
    lst6 = [0.2,0.2,0.3,0.1,0.1]

    print '1: ' + str(exclusive(lst1,100))
    print '2: ' + str(exclusive(lst2,100))
    print '3: ' + str(exclusive(lst3,100))
    print '4: ' + str(exclusive(lst4,100))
    print '5: ' + str(exclusive(lst5,100))
    print '6: ' + str(exclusive(lst6,100))
'''
