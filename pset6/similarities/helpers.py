from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    aSet = set(a.splitlines())
    bSet = set(b.splitlines())
    return aSet & bSet


def sentences(a, b):
    """Return sentences in both a and b"""
    aSet = set(sent_tokenize(a))
    bSet = set(sent_tokenize(b))
    return aSet & bSet


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    aSet = set(helper(a,n))
    bSet = set(helper(b,n))
    return aSet & bSet

def helper(x,n):
    substr = list()
    for i in range(len(x)-(n-1)):
        substr.append(x[i:i+(n)])
    return substr
