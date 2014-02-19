#!/usr/bin/python

"""
General problem solver
"""

class queue:
  def __init__(self):
    self.q = []

  def empty(self):
    return self.q == []
    
  def enqueue(self, x):
    self.q.append(x)

  def dequeue(self):
    if self.empty():
      raise Exception("Empty queue")
    else:
      ret = self.q[0]
      self.q = self.q[1:]
      return ret

class ProblemSolver:
  def __init__(self):
    # Dictionary mapping states to the path to them, used by derived classes
    self.history = {}
    
  def startState(self):
    raise Exception("Not implemented")

  def isSolutionState(self):
    raise Exception("Not implemented")

  def generator(self, state):
    raise Exception("Not implemented")

  def _findOneSolution(self, curState):
    """
    Returns None if no solution is found
    """
    
    if self.isSolutionState(curState):
      return curState
    else:
      nextStates = self.generator(curState)
      for s in nextStates:
          res = self._findOneSolution(s)
          # returns the first good solution found
          if res is not None:
            return res
      # returns None when no solution is found or we are at a dead end
      return None 
      
  def findOneSolution(self):
    self.history = {}
    self.history[self.startState()] = []
    return self._findOneSolution(self.startState())

  def _findAllSolutions(self, curState):
    """
    Returns a list of solutions
    """
    
    if self.isSolutionState(curState):
      return [curState]
    else:
      nextStates = self.generator(curState)
      # solutionSets is a list of lists of solutions (which in turn are lists)
      solutionsSets = map(lambda s: self._findAllSolutions(s), nextStates)
#      print solutionSets
      # XXX
      return reduce(lambda a,b:a+b, solutionsSets, [])
  
  def findAllSolutions(self):
    self.history = {}
    self.history[self.startState()] = []
    return self._findAllSolutions(self.startState())

  def findOneSolutionBFS(self):
    # initialize utility data structures
    q = queue()
    discoveredStates = set()
    self.history = {}
    print 'here'

    # add initial state to the queue
    q.enqueue(self.startState())
    self.history[self.startState()] = []
    

    while not q.empty():
      s = q.dequeue()
      print "Just exploring from",  s
      discoveredStates.add(s)
      if self.isSolutionState(s):
        return s
      else:
        newStates = filter(lambda x: x not in discoveredStates, self.generator(s))
        for newState in newStates:
          q.enqueue(newState)
    return None
    
    
    

# We represent a board as a list of 8 numbers representing the row (1-8) we place
# each queen. Example: In [3, 4, 6, 1, 3, 5, 8, 7] there is a queen at position (4, 2) 

class EightQueensSolver(ProblemSolver):
  
  def startState(self):
    # returns an empty board as an array
    return []

  def isSolutionState(self, board):
    def areQueensAttacking(r1, c1, r2, c2):
      """ Check whether the queens at (r1,c1) and (r2,c2) attack each other"""
      # an attack happens when the queen are:
      # (1) on the same row
      if r1 == r2: return True
      # (2) on the same column
      if c1 == c2: return True
      # (3) on the same diagonal
      if c1-c2 == r1-r2: return True
      return False
      
    if len(board) < 8:
      return False

    # check collisions, we use a naive check for all pairs
    for c1 in range(8-1):
      for c2 in range(c1+1,8):
        if areQueensAttacking(board[c1], c1, board[c2], c2):
          return False
    # No attacks        
    return True
  
  def generator(self, board):
    # remove Rows we already used for optimization
    newRows = set(range(1,8+1)).difference(board)
    newStates = map(lambda x: board+[x], newRows)    
    return newStates

queensSolver = EightQueensSolver()

def rotateBoard(board):
  # Using the following transformation
  # r' -> c
  # c' -> N-r+1
  N = 8
  rotatedBoard = [0]*8
  for c in range(N):
    rotatedBoard[ N - board[c] ] = c+1
  return rotatedBoard

def reflectBoardV(board):
  N = 8
  reflectedBoard = [0]*8
  for c in range(N):
    reflectedBoard[c] = N-board[c]+1
  return reflectedBoard

# XXX:
# Forget about this for a while
def reflectBoardH(board):
  N = 8
  reflectedBoard = [0]*8
  for c in range(N):
    reflectedBoard[c] = board[N-board[c]+1]
  return reflectedBoard
  
def generateSymmetries(board):
  l = [board]+[None]*3
  # gets all rotations
  for i in range(1,4):
    l[i] = rotateBoard(l[i-1])
  return l[1:]+[reflectBoardV(board)]

def checkAllSymmetries(solutions):
  for s in solutions[:]:
    symmetries = generateSymmetries(s)
    for sym in symmetries:
      if sym != s: solutions.remove(sym)

# XXX: mark discovered solutions (at least in BFS: the class below may generate states you already saw)

# Missionaries and cannibals problem



class MissionariesCannibals(ProblemSolver):
  LEFT_SIDE = -1
  RIGHT_SIDE = 1

  def startState(self):
    return (3, 3, self.LEFT_SIDE)
  
  def isSolutionState(self, state):
    return state == (0, 0, self.RIGHT_SIDE)

  def moveBoat(self, rowers, state):
    """
    Return a new state where rowers are moved and 
    boat position is updated 
    """
    
    (M,C,b) = state
    (m,c) = rowers
    return (M+m*b, C+c*b, b*(-1))

  def cannibalsCantEat(self, state):
    # check that, on both sides, cannibals can't take over
    (M,C,b) = state
    # example: (2, 2, b) means:
    #  - 2 missionaries and 2 cannibals on the left which is ok (2 >= 2)
    #  - 1 missionary and 1 cannibal (3-2 and 3-2)  which is ok (1 >= 1)
    # if there are zero missionaries it's okay too
    return (M >= C or M == 0) and (3-M >= 3-C or 3-M == 0)

  def generator(self, state):
    # (1,1) means a missionary and a cannibal rowing , (0,1) only a cannibal rowing and so on
    rowers = [(1, 1), (1, 0), (0, 1), (2,0), (0,2)]
# OLD CODE:  newStates = map(lambda r: self.moveBoat(r, state), rowers)
    newStates = []
    for r in rowers:
      newState = self.moveBoat(r, state)
      newStates.append(newState)
      if newState not in self.history:
        # update appending rowers to the old history
        self.history[newState] = (self.history[state] + [r])
    return filter(lambda s: self.cannibalsCantEat(s), newStates)

  def ppHistory(self, history):
    print "Solution of size", len(history), ":"
    side = -1
    for (m,c) in history:
      print "There are %d missionary(ies) and %d cannibal(s) rowing to the %s side of the river" % (m, c, side == -1 and "right" or "left")
      side = side*(-1)
      
    
def testMC():
  mc = MissionariesCannibals()
  solution = mc.findOneSolutionBFS()
  mc.ppHistory(mc.history[solution])
  return solution


    

# XXX
if __name__ == '__main__':
  pass
