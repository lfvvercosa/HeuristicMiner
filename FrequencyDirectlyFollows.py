class FrequencyDirectlyFollows:
    def __init__(self, log, act):
        self.ft = self.createFrequencyDict(log, act)
    

    def createFrequencyDict(self, log, act):
        if log is not None and act is not None:
            # create dict for counting
            d = {}
            for a in act:
                d[a] = 0
            ft = {}
            # create keys for all activities
            for a in act:
                ft[a] = d.copy()
            
            # count occurence of succesions (a > b)
            for l in log:
                for index, act in enumerate(l):
                    if index + 1 < len(l):
                        ft[act][l[index + 1]] += 1
            
            return ft
