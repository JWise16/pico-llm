import random
#import Shapes
#from Vector import *

ROWS = 20
COLUMNS = 20
EMPTY = False
OBSTACLE = True
MAXSTATES = 5
TRIALS = 20
STEPS = 800
MUTATIONRATE = 0.02
TOPFRACTION = 0.2
VALIDPATTERNS = ["xxxx", "Nxxx", "NExx", "NxWx", "xxxS", "xExS", "xxWS", "xExx", "xxWx"]
#RENDERMETHOD = "Shapes"

# This class defines a Picobot program.  The program is represented internally as a dictionary
# with keys of the form (state, pattern) and values of the form (move, state) where pattern is one
# of the valid patterns in the list VALIDPATTERS, state is a number in the range from 0 to MAXSTATES-1,
# and move is an element of ["N", "E", "W", "S"].

class Program:
    def __init__(self):
        self.rulesDict = {}

    def randomize(self):
        """ Constructs a random program """
        for state in range(MAXSTATES):
            for pattern in VALIDPATTERNS:
                nextstate = random.randint(0, MAXSTATES-1)
                possibleMoves= ["N", "E", "W", "S"]
                for char in pattern:
                    if char != "x": possibleMoves.remove(char)
                move = random.choice(possibleMoves)
                self.rulesDict[(state, pattern)] = (move, nextstate)

    def getMove(self, state, pattern):
        """ Given a state and pattern string, returns a tuple of the form (newstate, move)
        indicating the move associated with that state and pattern."""
        return self.rulesDict[(state, pattern)] 
    
    def mutate(self):
        """ Mutate the program by replacing one line of the program with another random line."""
        pattern = random.choice(VALIDPATTERNS)
        startState = random.randint(0, MAXSTATES-1)
        possibleMoves = ["N", "E", "W", "S"]
        for char in pattern:
            if char != "x": possibleMoves.remove(char)
        move = random.choice(possibleMoves)
        nextState = random.randint(0, MAXSTATES-1)
        self.rulesDict[(startState, pattern)]=(move,nextState)

    def crossover(self, other):
        """ Crosses self with other, returning a new program object """
        D = {}
        crossPoint = random.randint(0, MAXSTATES-1)
        for state in range(MAXSTATES):
            for pattern in VALIDPATTERNS:
                if state <= crossPoint:
                    D[(state, pattern)] = self.rulesDict[(state, pattern)]
                else:
                    D[(state, pattern)] = other.rulesDict[(state, pattern)]
        offspring = Program()
        offspring.rulesDict = D
        return offspring

    def __repr__(self):
        output = ""
        for key in self.rulesDict.keys():
            value = self.rulesDict[key]
            output = output + str(key[1]) + " " + str(key[0]) + " -> " + str(value[0]) + " " + str(value[1]) + "\n"
        return output
        
class cell:
    def __init__(self):
        self.visited = False

class Picobot:
    def __init__(self, picobotrow, picobotcol, program):
        self.program = program # self stores a Program object
        self.array = [] # This will be an array of the empty cells in the room
        for r in range(ROWS):
            row = []
            for c in range(COLUMNS):
                row.append(cell())
            self.array.append(row)
        self.robotRow = picobotrow  # row
        self.robotCol = picobotcol  # column
        self.state = 0  # starts in state 0!
        self.array[picobotrow][picobotcol].visited = True  #We've visited this cell
        self.numVisited = 1  # visited one cell so far

    def step(self):
        # Take one step according to the self.rules
        pattern = ""
        if self.robotRow == 0:
            pattern = pattern + "N"
        else:
            pattern = pattern + "x"
        if self.robotCol == COLUMNS-1:
            pattern = pattern + "E"
        else:
            pattern = pattern + "x"
        if self.robotCol == 0:
            pattern = pattern + "W"
        else:
            pattern = pattern + "x"
        if self.robotRow == ROWS - 1:
            pattern = pattern + "S"
        else:
            pattern = pattern + "x"
        output = self.program.getMove(self.state, pattern)
        direction = output[0]
        self.state = output[1]
        if direction == "N":
            self.robotRow = self.robotRow - 1
        elif direction == "E":
            self.robotCol = self.robotCol + 1
        elif direction == "W":
            self.robotCol = self.robotCol - 1
        else:
            self.robotRow = self.robotRow + 1
        if self.robotRow < 0 or self.robotRow >= ROWS or self.robotCol < 0 or self.robotCol >= COLUMNS:
            return False
        if not self.array[self.robotRow][self.robotCol].visited:
            self.numVisited += 1
            self.array[self.robotRow][self.robotCol].visited = True

    def run(self, steps):
        # Run the program for the given number of steps
        for x in range(steps):
            self.step()

    def __repr__(self):
        output = "*"*(COLUMNS+2) + "\n"
        for r in range(ROWS):
            output = output + "*"  # left wall
            for c in range(COLUMNS):
                if self.robotRow == r and self.robotCol == c:
                    output = output + "P"
                elif self.array[r][c].visited:
                    output = output + "."
                else:
                    output = output + " "
            output = output + "*\n"  # right wall and line break
        output = output + "*"*(COLUMNS+2) + "\n" 
        return output

# This is the acual program

def randomPopulation(size):
    """ Make a list (population) of Programs and return this list """
    population = []
    for n in range(size):
        newProgram = Program()
        newProgram.randomize()
        population.append(newProgram)
    return population

def evaluateFitness(program, trials, trialLength):
    """ Evaluate the fitness of a rule set by running it trials times, each time
    for trialLength steps, and return a number between 0 and 1 indicating the average
    fraction of the room that this rule set visited."""
    scoreCounter = 0
    for x in range(trials):
        p = Picobot(random.randint(0, ROWS-1), random.randint(0, COLUMNS-1), program)
        p.run(trialLength)
        scoreCounter += p.numVisited
    return (1.0*scoreCounter/trials)/(ROWS*COLUMNS) # fitness score

def rank(population):
    """ Takes as input a population of rule sets and returns a list of form (score, rule set)
    where the score is between 0 (low) and 1 (high)"""
    scored = [(evaluateFitness(program, TRIALS, STEPS), program) for program in population]
    scored.sort()
    scored.reverse()
    return scored

def render(program, steps):
    SIDE = 20

    # Render boundary of room
    for col in range(COLUMNS): # Render top and bottom of room
        top = Shapes.Square(SIDE, center=Vector(col*SIDE, ROWS*SIDE), color = "blue")
        top.render()
        bottom = Shapes.Square(SIDE, center=Vector(col*SIDE, -1*SIDE), color = "blue")
        bottom.render()
    for row in range(-1,ROWS+1): # Render left and right sides
        left = Shapes.Square(SIDE, center=Vector(-1*SIDE,row*SIDE), color = "blue")
        left.render()
        right = Shapes.Square(SIDE, center=Vector(COLUMNS*SIDE, row*SIDE), color="blue")
        right.render()

    # Make a new picobot
    p = Picobot(random.randint(0, ROWS-1), random.randint(0, COLUMNS-1), program)
    for s in range(steps):
        r = p.robotRow # Get the picbot's row
        c = p.robotCol # ... and column
        picoBox = Shapes.Square(SIDE, center=Vector(c*SIDE, (ROWS-1-r)*SIDE), color="green")
        picoBox.render()
        picoBox.color="gray"
        picoBox.render()
        p.step()

                        
def GA(popSize, generations):
    print "Grid size being used is ", ROWS, " by ", COLUMNS
    print "Fitness is measured using", TRIALS, "random trials and running for", STEPS, "steps"
    currentGeneration = randomPopulation(popSize)
    for gen in range(generations):
        scored = rank(currentGeneration)
        scores = [X[0] for X in scored]
        print "Generation ", gen
        print "  Average fitness: ", sum(scores)/popSize
        print "  Best fitness: ", max(scores)
        cutoff = int(popSize * TOPFRACTION)
        best = scored[0:cutoff] # Take the best TOPFRACTION of the population for reproduction
        nextGeneration = []
        for i in range(popSize):
            program1 = random.choice(best)[1]
            program2 = random.choice(best)[1]
            offspring = program1.crossover(program2)
            if random.uniform(0, 1) < MUTATIONRATE:  offspring.mutate()
            nextGeneration.append(offspring)
        currentGeneration = nextGeneration
    bestProgram = rank(currentGeneration)[0][1]
    print bestProgram
#    if RENDERMETHOD == "Shapes":
#        render(bestProgram, 500)
        
    
    
    
        
    

    

        
