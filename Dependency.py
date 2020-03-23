class Dependency:
    def __init__(self, ft, act):
        self.dt = self.createDependencyTable(ft, act)
    
    def createDependencyTable(self, ft, act):
        if ft is not None and act is not None:
            # create dict for counting
            d = {}
            for a in act:
                d[a] = 0
            dt = {}
            # create keys for all activities
            for a in act:
                dt[a] = d.copy()

            for a in act:
                for b in act:
                    if a != b:
                        dt[a][b] = round((ft[a][b] - ft[b][a]) / \
                            (ft[a][b] + ft[b][a] + 1),2)
                    if a == b:
                        dt[a][b] = ft[a][b]/(ft[a][b] + 1)

            return dt
