from Log import Log
from Activity import Activity
from FrequencyDirectlyFollows import FrequencyDirectlyFollows
from Dependency import Dependency
from CNet import CNet
from Util import preProcessLog

# Implementation base on book: Process Mining by Wil van der Aalst (second edition)
# pages: Chapter 3 -> Causal Nets (page 72)
# pages: Chapter 7 -> Heuristic Miner (page 201)

def main(l, params):

    act = Activity(l)
    
    l = preProcessLog(l, act.a)

    print("")
    print("############## ACTIVITIES SET ##############")
    act = Activity(l)
    print(act.a)

    print("")
    print("############## LOG LIST ##############")
    log = Log(l)
    print(log.l)

    print("")
    print("############## FREQUENCY TABLE ##############")
    freq = FrequencyDirectlyFollows(log.l, act.a)
    print(freq.ft)

    print("")
    print("############## DEPENDENCY TABLE ##############")
    depen = Dependency(freq.ft, act.a)
    print(depen.dt)

    print("")
    print("############## CNET A_I AND A_O ##############")
    cnet = CNet(act.a, log.l, freq.ft, depen.dt, params)
    print(cnet.a_i)
    print(cnet.a_o)

    print("")
    print("############## CNET DEPENDENCY OUT ##############")
    print(cnet.depRelOut)

    print("")
    print("############## CNET DEPENDENCY IN ##############")
    print(cnet.depRelIn)

    print("")
    print("############## CNET OUTPUT BINDINGS ##############")
    print(cnet.outBind)
 
    print("")
    print("############## CNET INPUT BINDINGS ##############")
    print(cnet.inBind)

    print("")
    print("############## CNET IS VALID SEQUENCE ##############")
    print(cnet.isValidSequence(['a','b','b','e'], 4))

l = [
    ['a', 'e'],
    ['a', 'e'],
    ['a', 'e'],
    ['a', 'e'],
    ['a', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'b', 'c', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'c', 'b', 'e'],
    ['a', 'b', 'e'],
    ['a', 'c', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],
    ['a', 'd', 'e'],    
    ['a', 'd', 'd', 'e'],
    ['a', 'd', 'd', 'e'],
    ['a', 'd', 'd', 'd', 'e'],  
    ]

# l = [
#     ['c','b','a','d','e'],
#     ['b','c','a','e','d'],
#     ['b','c','a','e'],
#     ['c','b','a','e'],
#     ['b','c','a','d','e']

#     ]

params = {
         'freqThreshold' : 2,
         'depThreshold' : 0.7,
         'windowSize' : 4,
         'bindThreshold' : 2,
         }

main(l, params)

