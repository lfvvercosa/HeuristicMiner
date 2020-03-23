from collections import OrderedDict

class CNet:
    def __init__(self, act, log, freq, dep, params):
        self.act = act
        self.a_i = log[0][0]
        self.a_o = log[0][-1]

        (self.depRelOut, self.depRelIn) = self.dependenceRelation(act, 
                                                                  freq, 
                                                                  dep, 
                                                                  params['freqThreshold'],
                                                                  params['depThreshold'])
        
        self.outBind = self.findOutputBindings(log,
                                               act,
                                               self.depRelOut,
                                               params['windowSize'],
                                               params['bindThreshold'])
        
        self.inBind = self.findInputBindings(log,
                                             act,
                                             self.depRelIn,
                                             params['windowSize'],
                                             params['bindThreshold'])

    def dependenceRelation(self, 
                           act,
                           freq, 
                           dep, 
                           freqThreshold,
                           depThreshold):
        
        depRelOut = {}
        depRelIn = {}

        for a in act:
            depRelOut[a] = []
            depRelIn[a] = []

        for a in act:
            for b in act:
                if freq[a][b] > freqThreshold and \
                   dep[a][b] > depThreshold:
                   depRelOut[a].append(b)
                   depRelIn[b].append(a)

        return (depRelOut, depRelIn)

    
    def isInFollowedList(self, a, l, depRel):
        for b in l:
            if a in depRel[b]:
                return True
        
        return False

    def getOutActivitiesInWindow(self, log, a, index, window, depRelOut):
           follows = log[(index+1):(index+1+window)]
           follows = [b for b in follows if b in depRelOut[a]]
           follows = list(OrderedDict.fromkeys(follows))

           for idx, b in enumerate(follows):
               if self.isInFollowedList(b, follows[:idx], depRelOut):
                   follows.remove(b)

           return follows


    def filterLessFreqBindings(self, logAssociatedBind, bind, bindThreshold):
        hasFiltered = True
        
        while(hasFiltered):

            hasFiltered = False

            for key in bind:
                for key2 in list(bind[key]):
                    if bind[key][key2] < bindThreshold:
                        bind[key].pop(key2, None)
                        for e in logAssociatedBind:
                            if (key, key2) in logAssociatedBind[e]:
                                hasFiltered = True
                                logAssociatedBind[e].remove((key, key2))
                                for b in logAssociatedBind[e]:
                                    bind[b[0]][b[1]] -= bindThreshold - 1
        

        return bind


    def findOutputBindings(self,
                           log,
                           act,
                           depRelOut,
                           windowSize,
                           bindThreshold):
        outBind = {}
        # used for filtering less frequent bindings
        logAssociatedOutBind = {}

        for a in act:
            outBind[a] = {}

        for l in log:
            for idx, a in enumerate(l):
                follows = self.getOutActivitiesInWindow(l,
                                                        a, 
                                                        idx, 
                                                        windowSize,
                                                        depRelOut)
                follows.sort()
                key = str(follows)

                if key in outBind[a]:
                    outBind[a][key] += 1
                else:
                    outBind[a][key] = 1

                key2 = str(l)

                if key2 not in logAssociatedOutBind:
                    logAssociatedOutBind[key2] = []

                if (a, key) not in logAssociatedOutBind[key2]:
                    logAssociatedOutBind[key2].append((a,key))
        
         
        return self.filterLessFreqBindings(logAssociatedOutBind, 
                                           outBind, 
                                           bindThreshold)


    def isInPreviousList(self, a, l, depRelIn):
        for b in l:
            if a in depRelIn[b]:
                return True

        return False


    def getInActivitiesInWindow(self, log, a, index, window, depRelIn):
        previous = log[max(0,(index-window)):index]
        previous = [b for b in previous if b in depRelIn[a]]
        # remove repeated
        previous = list(OrderedDict.fromkeys(previous))

        for idx, b in enumerate(previous):
            if self.isInPreviousList(b, previous[idx+1:], depRelIn):
                previous.remove(b)

        return previous


    def findInputBindings(self,
                           log,
                           act,
                           depRelIn,
                           windowSize,
                           bindThreshold):
        inBind = {}
        # used for filtering less frequent bindings
        logAssociatedInBind = {}

        for a in act:
            inBind[a] = {}

        for l in log:
            for idx, a in enumerate(l):
                previous = self.getInActivitiesInWindow(l,
                                                       a,
                                                       idx,
                                                       windowSize,
                                                       depRelIn)
                previous.sort()
                key = str(previous)

                if key in inBind[a]:
                    inBind[a][key] += 1
                else:
                    inBind[a][key] = 1

                key2 = str(l)

                if key2 not in logAssociatedInBind:
                    logAssociatedInBind[key2] = []

                if (a, key) not in logAssociatedInBind[key2]:
                    logAssociatedInBind[key2].append((a, key))

        return self.filterLessFreqBindings(logAssociatedInBind,
                                           inBind,
                                           bindThreshold)


    def isValidSequence(self, l, windowSize):

        obligations = []

        for idx, a in enumerate(l):
            previous = self.getInActivitiesInWindow(l,
                                                    a,
                                                    idx,
                                                    windowSize,
                                                    self.depRelIn)

            follows = self.getOutActivitiesInWindow(l,
                                                    a,
                                                    idx,
                                                    windowSize,
                                                    self.depRelOut)

            previous = list(set(previous))
            follows = list(set(follows))

            print(a, previous, follows)

            if idx == 0:
                if previous != []:
                    return False
                
                if a != self.a_i:
                    return False

            if idx == len(l) - 1:
                if follows != []:
                    return False
                
                if a != self.a_o:
                    return False

            for b in previous:
                try:
                    obligations.remove((b, a))
                except:
                    return False

            for b in follows:
                try:
                    obligations.append((a, b))
                except:
                    return False

            print('obligations: ', [obligations])

        return True

