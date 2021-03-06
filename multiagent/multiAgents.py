# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [
            self.evaluationFunction(
                gameState,
                action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(
                len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentFood = currentGameState.getFood().asList()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]
        newFood = newFood.asList()
        score = 0
        closest = 999999999999
        for pos in newFood:
            dist = manhattanDistance(newPos, pos)
            score += 2 / (1 + dist)
            if dist < closest:
                closest = dist
        score -= closest
        if len(currentFood) > len(newFood):
            score += 10
        for i in range(len(newGhostStates)):
            if newScaredTimes[i] > 1:
                score += 1 / \
                    (1 + manhattanDistance(newGhostStates[i].getPosition(), newPos))
            else:
                score -= 1 / \
                    (1 + manhattanDistance(newGhostStates[i].getPosition(), newPos))
        if successorGameState.isWin():
            score = 99999999
        return score + successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          Directions.STOP:
            The stop direction, which is always legal

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        depth = self.depth
        return self.rootNode(gameState, 1)


    def rootNode(self, gameState, depth):
        moves = gameState.getLegalActions(0)
        vals = list()
        for move in moves:
            newState = gameState.generateSuccessor(0, move)
            if newState.isWin() or newState.isLose():
                vals.append(self.evaluationFunction(newState))
            else:
                vals.append(self.minNode(newState, depth, 1))
        return moves[vals.index(max(vals))]

    def maxNode(self, gameState, depth):
        moves = gameState.getLegalActions(0)
        vals = list()
        for move in moves:
            newState = gameState.generateSuccessor(0, move)
            if newState.isWin() or newState.isLose():
                vals.append(self.evaluationFunction(newState))
            else:
                vals.append(self.minNode(newState, depth, 1))
        return max(vals)


    def minNode(self, gameState, depth, agentNum):
        moves = gameState.getLegalActions(agentNum)
        vals = list()
        if agentNum == gameState.getNumAgents()-1 and depth == self.depth:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                vals.append(self.evaluationFunction(newState))
            return min(vals)
        if agentNum == gameState.getNumAgents()-1:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                if newState.isWin() or newState.isLose():
                    vals.append(self.evaluationFunction(newState))
                else:
                    vals.append(self.maxNode(newState, depth+1))
            return min(vals)
        else:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                if newState.isWin() or newState.isLose():
                    vals.append(self.evaluationFunction(newState))
                else:
                    vals.append(self.minNode(newState, depth, agentNum+1))
            return min(vals)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        depth = self.depth
        return self.rootNode(gameState, 1, -999999999999, 999999999999)


    def rootNode(self, gameState, depth, alpha, beta):
        moves = gameState.getLegalActions(0)
        vals = list()
        v = -9999999999
        for move in moves:
            newState = gameState.generateSuccessor(0, move)
            if newState.isWin() or newState.isLose():
                vals.append(self.evaluationFunction(newState))
            else:
                vals.append(self.minNode(newState, depth, 1, alpha, beta))
            v = max(v, vals[-1])
            if v > beta:
                return moves[vals.index(v)]
            alpha = max(alpha,v)
        return moves[vals.index(v)]

    def maxNode(self, gameState, depth, alpha, beta):
        moves = gameState.getLegalActions(0)
        vals = list()
        v = -9999999999
        for move in moves:
            newState = gameState.generateSuccessor(0, move)
            if newState.isWin() or newState.isLose():
                vals.append(self.evaluationFunction(newState))
            else:
                vals.append(self.minNode(newState, depth, 1, alpha, beta))
            v = max(v, vals[-1])
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v


    def minNode(self, gameState, depth, agentNum, alpha, beta):
        moves = gameState.getLegalActions(agentNum)
        vals = list()
        v = 99999999999
        if agentNum == gameState.getNumAgents()-1 and depth == self.depth:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                vals.append(self.evaluationFunction(newState))
                v = min(v, vals[-1])
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        if agentNum == gameState.getNumAgents()-1:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                if newState.isWin() or newState.isLose():
                    vals.append(self.evaluationFunction(newState))
                else:
                    vals.append(self.maxNode(newState, depth+1, alpha, beta))
                v = min(v, vals[-1])
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        else:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                if newState.isWin() or newState.isLose():
                    vals.append(self.evaluationFunction(newState))
                else:
                    vals.append(self.minNode(newState, depth, agentNum+1, alpha, beta))
                v = min(v, vals[-1])
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        depth = self.depth
        return self.rootNode(gameState, 1)


    def rootNode(self, gameState, depth):
        moves = gameState.getLegalActions(0)
        vals = list()
        for move in moves:
            newState = gameState.generateSuccessor(0, move)
            if newState.isWin() or newState.isLose():
                vals.append(self.evaluationFunction(newState))
            else:
                vals.append(self.minNode(newState, depth, 1))
        return moves[vals.index(max(vals))]

    def maxNode(self, gameState, depth):
        moves = gameState.getLegalActions(0)
        vals = list()
        for move in moves:
            newState = gameState.generateSuccessor(0, move)
            if newState.isWin() or newState.isLose():
                vals.append(self.evaluationFunction(newState))
            else:
                vals.append(self.minNode(newState, depth, 1))
        return max(vals)


    def minNode(self, gameState, depth, agentNum):
        moves = gameState.getLegalActions(agentNum)
        vals = list()
        if agentNum == gameState.getNumAgents()-1 and depth == self.depth:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                vals.append(self.evaluationFunction(newState))
            return sum(vals)/len(vals)
        if agentNum == gameState.getNumAgents()-1:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                if newState.isWin() or newState.isLose():
                    vals.append(self.evaluationFunction(newState))
                else:
                    vals.append(self.maxNode(newState, depth+1))
            return sum(vals)/len(vals)
        else:
            for move in moves:
                newState = gameState.generateSuccessor(agentNum, move)
                if newState.isWin() or newState.isLose():
                    vals.append(self.evaluationFunction(newState))
                else:
                    vals.append(self.minNode(newState, depth, agentNum+1))
            return sum(vals)/len(vals)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      So for this one I actually just copied the evaluation function that I had for
      q1 because that actually worked pretty well, and it seems to work pretty consistently
      (knock on wood, hopefully it's consistent when it matters lol)

      There are a few differences though:
      I changed successorGameState to currentGameState so I didn't have to refactor everything lol
      I added the time each ghost is scared to encourage pellet eating because I'm pretty sure that increases score
    """
    successorGameState = currentGameState
    currentFood = currentGameState.getFood().asList()
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [
        ghostState.scaredTimer for ghostState in newGhostStates]
    newFood = newFood.asList()
    score = 0
    closest = 999999999999
    for pos in newFood:
        dist = manhattanDistance(newPos, pos)
        score += 2 / (1 + dist)
        if dist < closest:
            closest = dist
    score -= closest
    if len(currentFood) > len(newFood):
        score += 10
    for i in range(len(newGhostStates)):
        if newScaredTimes[i] > 1:
            score += 2 / \
                (1 + manhattanDistance(newGhostStates[i].getPosition(), newPos))
        else:
            score -= 1 / \
                (1 + manhattanDistance(newGhostStates[i].getPosition(), newPos))
    for time in newScaredTimes:
        score += time/2
    if successorGameState.isWin():
        score = 99999999
    return score + successorGameState.getScore()


# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
