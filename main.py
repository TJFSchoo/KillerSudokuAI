sudokuToSolve = [
    [0,0,0,0,0,0,6,1,9],
    [0,2,3,0,9,0,0,0,0],
    [0,0,0,1,4,0,0,2,0],
    [0,0,9,0,0,0,0,0,0],
    [7,0,8,0,0,3,0,0,0],
    [0,0,0,0,0,5,3,4,0],
    [0,0,0,0,0,0,4,6,7],
    [8,3,0,0,0,0,0,0,0],
    [0,0,0,6,1,2,0,0,0]
]

# AI
def solve(board):
    foundEmptySquare = findEmpty(board)
    if not foundEmptySquare:
        # Als er geen lege vakjes meer zijn is de puzzel opgelost
        return True
    else:
        row, col = foundEmptySquare

    for i in range(1,10):
        if checkValidity(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

# Functie om met Constraint Satisfaction te valideren of zet valide is (Boolean)
def checkValidity(board, num, pos):
    # Constraint op rij (horizontaal)
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Constraint op kolom (verticaal)
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Constraint op vierkant (9x9)
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def printBoard(board):
    for i in range(len(board)):
        # Na elke derde rij een horizontale streep
        if i % 3 == 0 and i != 0:
            print("--------------------------- ")

        # Na elk derde getal een verticale streep
        for j in range(len(board[0])):
            # !=0 vanwege geen streep aan de buitenkant, end="" zorgt ervoor dat er geen backslash (naar volgende regel springen) komt
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            # einde v/d regel
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

# Functie voor het afgaan van vakjes van een board, op zoek naar nog niet ingevulde vakjes
def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # rij, kolom

    return None

printBoard(sudokuToSolve)
solve(sudokuToSolve)
print("___________________")
printBoard(sudokuToSolve)