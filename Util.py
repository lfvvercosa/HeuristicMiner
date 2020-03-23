def findAllInitActivity(log):
        return list(set([l[0] for l in log]))


def findOrCreateInitActivity(log):
    init = findAllInitActivity(log)
    if len(init) > 1:
        return 'a_i'
    else:
        return init[0]


def findAllEndActivity(log):
    return list(set([l[-1] for l in log]))


def findOrCreateEndActivity(log):
    end = findAllEndActivity(log)
    if len(end) > 1:
        return 'a_o'
    else:
        return end[0]


def preProcessLog(log, act):
    if log is not None:

        initAct = findOrCreateInitActivity(log)
        endAct = findOrCreateEndActivity(log)

        if initAct not in act:
            for l in log:
                l.insert(0,initAct)
        
        if endAct not in act:
            for l in log:
                l.insert(len(l), endAct)


        return log

            
