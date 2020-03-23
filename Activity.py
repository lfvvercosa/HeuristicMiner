class Activity:

    def __init__(self, log):
        self.a = self.activitySet(log)
    
    def activitySet(self, log):
        a = []
        if log is not None:
            for l in log:
                a = a + l
        return set(a)
