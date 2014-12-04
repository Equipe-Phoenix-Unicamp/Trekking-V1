class StateMachine:
    """The machine that will run the assigned States to it.
A state name may not ever be 'stop', its a reserved keyword to stop the machine execution"""
    def __init__(self):
        self.states = {}
        self.args = {}

    def addState(self, state, stateName):
        self.states[stateName] = state

    def setStartState(self, stateName):
        self.startState = stateName

    def start(self):
        print "state Machine Started"
        currentState = self.startState
        self.states[currentState].onStart(self.args)
        while True:
            nextState = self.states[currentState].run(self.args)
            if nextState == "stop":
                self.states[currentState].onEnd(self.args)
                print "State Machine Stopped"
                break
            elif nextState != currentState:
                self.states[currentState].onEnd(self.args)
                self.states[nextState].onStart(self.args)

class State:
    def __init__(self):
        self.onStart
        self.onEnd
        self.run

    def _start(self, args):
        return
    def _end(self, args):
        return
    def _run(self, args):
        return "stop"

    run = _run
    onStart = _start
    onEnd = _end
    

class TestState(State):
    def _start(self, args):
        print "start"
    def _run(self, args):
        print "run"
        return "estado"
    def _end(self, args):
        print "end"

    run = _run
    onStart = _start
    onEnd = _end
