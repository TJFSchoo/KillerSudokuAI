solutionGrid = [
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0]
]

killerSudokuGrid = [
    [3,  3,  15, 15, 15, 22, 4,  16, 15],
    [25, 25, 17, 17, 22, 22, 4,  16, 15],
    [25, 25, 9,  9,  22, 8,  20, 20, 15],
    [6,  14, 14, 9,  17, 8,  20, 17, 15],
    [6,  13, 13, 20, 17, 8,  17, 17, 12],
    [27, 13, 6,  20, 17, 20, 6,  6,  12],
    [27, 6,  6,  20, 10, 20, 20, 14, 14],
    [27, 8,  16, 10, 10, 15, 15, 14, 14],
    [27, 8,  16, 10, 13, 13, 13, 17, 17]
]

# AI
def solve(solutionGrid, killerGrid):
    foundEmptySquare = findEmpty(solutionGrid)
    if not foundEmptySquare:
        # Als er geen lege vakjes meer zijn is de puzzel opgelost
        return True
    else:
        row, col = foundEmptySquare

    for i in range(1,10):
        if checkValidity(solutionGrid, i, (row, col), killerGrid):
            solutionGrid[row][col] = i

            if solve(solutionGrid):
                return True

            solutionGrid[row][col] = 0

    return False

# Functie om met Constraint Satisfaction te valideren of zet valide is (Boolean)
def checkValidity(board, numberFilledIn, position, killerGrid):
    # board[0] = horizontale waarde (row)
    # board[1] = verticale waarde (col)
    print("Number filled in: ")
    print(numberFilledIn)
    print("Position: ")
    print(position)

    # Constraint op rij (horizontaal)
    # Voor elke horizontale waarde wordt gekeken of het getal niet hetzefde is als het ingevulde nummer, met uitzondering van de plek die net is ingevuld
    for i in range(len(board[0])):
        if board[position[0]][i] == numberFilledIn and position[1] != i:
            return False

    # Constraint op kolom (verticaal)
    # Voor elke verticale waarde wordt gekeken of het getal niet hetzefde is als het ingevulde nummer, met uitzondering van de plek die net is ingevuld
    for i in range(len(board)):
        if board[i][position[1]] == numberFilledIn and position[0] != i:
            return False

    # Constraint op vierkant (9x9)
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == numberFilledIn and (i, j) != position:
                return False

    # Constraint op Killer squares
    print("Cage value:")
    print(killerGrid[position[0]][position[1]])
    print("len(board[0]):")
    print(len(board[0]))
    cageValue = killerGrid[position[0]][position[1]]
    killerCage = []

    # List aanvullen met alle aanliggende coordinaten die bij de killer cage horen
    # Eerst horizontaal checken, bij elke horizontale match ook verticaal checken
    # Voor iedere horizontale waarde: ( -> 1-9)
    for i in range(len(board[0])):
        if killerGrid[position[0]][i] == cageValue and position[1] != i:
            killerCage.append((0, i))
            print("Found horizontal cage match:")
            print((0, i))
            for v in range(len(board[i])):
                if killerGrid[v][position[1]] == cageValue and position[0] != i:
                    killerCage.append((v, [position[1]]))
                    print("Found vertical cage match:")
                    print((v, position[1]))

    # Als cage nog niet compleet is ingevuld, skip
    emptySpaceInCage = 0
    for i in range(killerCage):
        if board[position[i]] == 0:
            emptySpaceInCage = 1

    if emptySpaceInCage == 0:
        cageCount = 0
        # Optellen alle waardes en vergelijken met totale waarde die cage moet zijn bij oplossing
        for i in range(killerCage):
            cageCount = cageCount + board[position[i]]
        # Als alle cage waardes zijn ingevuld en de totale cage waarde wijkt af: False
        if cageValue != cageCount:
            return False

    return True

def printSolutionGrid(solutionGrid):
    for i in range(len(solutionGrid)):
        # Na elke derde rij een horizontale streep
        if i % 3 == 0 and i != 0:
            print("------ ------- ------")

        # Na elk derde getal een verticale streep
        for j in range(len(solutionGrid[0])):
            # !=0 vanwege geen streep aan de buitenkant, end="" zorgt ervoor dat er geen backslash (naar volgende regel springen) komt
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            # einde v/d regel
            if j == 8:
                print(solutionGrid[i][j])
            else:
                print(str(solutionGrid[i][j]) + " ", end="")

# Functie voor het afgaan van vakjes van een board, op zoek naar nog niet ingevulde vakjes
def findEmpty(solutionGrid):
    for i in range(len(solutionGrid)):
        for j in range(len(solutionGrid[0])):
            if solutionGrid[i][j] == 0:
                return (i, j)  # rij, kolom
    return None

print("Start:")
printSolutionGrid(solutionGrid)
solve(solutionGrid, killerSudokuGrid)
print(" ")
print("Oplossing:")
printSolutionGrid(solutionGrid)
