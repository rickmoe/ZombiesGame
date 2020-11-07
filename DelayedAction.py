class DelayedAction:

    instances = []

    def __init__(self, delayedActions=None):
        if delayedActions is None:
            delayedActions = [[]]
        self.delayedActions = delayedActions    # [[t1, action1, args1], [t2, action2, args2]...]
        self.t = 0
        DelayedAction.instances.append(self)

    def tick(self):
        for delayedAction in self.delayedActions:
            if delayedAction[0] <= self.t:
                delayedAction[1](*delayedAction[2])
                self.delayedActions.remove(delayedAction)
        self.t += 1
        if self.delayedActions == [[]]:
            DelayedAction.instances.remove(self)

    @staticmethod
    def getInstances():
        return DelayedAction.instances