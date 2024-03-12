def read_FEN(fen_str:str) -> dict:
    '''
    FEN -> Forsyth-Edwards Notation

    eg. rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2

    uppercase -> white
    lowercase -> black
    / -> next row
    [1-8] -> no. of spaces
    '''

    piece_position = {}

    position, player_to_move, castle_ability, en_pass_target_sqr, half_move, full_move = fen_str.split()

    row_num = 8
    for row in position.split("/"):
        col_num = 0

        for box in row:
            if box.isdigit():
                col_num += int(box)
                continue

            elif box.isupper():
                piece_position[chr(col_num + 65) + str(row_num)] = box.lower() + 'l'
            else:
                piece_position[chr(col_num + 65) + str(row_num)] = box + 'd'

            col_num += 1

        row_num -= 1
    return piece_position

'''

eg: 
{'A8': 'rd', 'B8': 'nd', 'C8': 'bd', 'D8': 'qd', 'E8': 'kd', 'F8': 'bd', 'G8': 'nd', 'H8': 'rd',
 'A7': 'pd', 'B7': 'pd', 'C7': 'pd', 'D7': 'pd', 'E7': 'pd', 'F7': 'pd', 'G7': 'pd', 'H7': 'pd', 
 'A2': 'pl', 'B2': 'pl', 'C2': 'pl', 'D2': 'pl', 'E2': 'pl', 'F2': 'pl', 'G2': 'pl', 'H2': 'pl', 
 'A1': 'rl', 'B1': 'nl', 'C1': 'bl', 'D1': 'ql', 'E1': 'kl', 'F1': 'bl', 'G1': 'nl', 'H1': 'rl'}

'''

#Sample values , to be changes one js python communication is active
board = read_FEN('8/p7/4R1k1/7p/8/8/1N2P2K/8 w KQkq - 0 1')
Piece = 'rw'
Piece_position = 'E6'


#A function which will determine the piece and output a list of all legal moves for the piece
def legalMove(piece_position , selectedPiece , selectedPiece_position):

    #Defining Row and Column of Piece

    column = selectedPiece_position[0] #A-H
    row = selectedPiece_position[1] #1-8

    if selectedPiece[0] == 'r': #Defining Rules for rook ('r')
        '''
        To check all legal moves for a rook we will:-
        -> Run a pointer in NSEW directions
        -> If the pointer reaches a box with a piece, legal moves in the 
           direction will extend from orignial position to 1 - the current 
           position of the pointer
        -> If the piece reaches the end of the board (A , H columns and 1,8 row we stop the pointer and add that position(if it is empty) and teriminate loop)
        -> Moving horizontally row value is constant and column value is changes by 1 every iteration. Since column is in
        letter we change the ASCII value
        -> Moving vertically column value is constant and row value is increased by 1 every iteration.
        ->if a columb in 'A' or 'B' or if a row is '1' or '8' it will check that square and then break the loop for that direction

        '''
        print(piece_position)

        pointer_east = pointer_west = pointer_north = pointer_south = 0 #Initial Pointer Position

        legalMoves = []

        east_f = west_f = north_f = south_f = True
        while east_f or west_f or north_f or south_f:
            if east_f:  
                pointer_east += 1 #Moving 1 step left
                new_piece_position =  chr(int(ord(column)) - pointer_east) + row #Moving across a row , column changes and row is constant
                if new_piece_position not in board: #If there is no piece in the current position of pointer, that square won't exist in the piece position dictionary
                    legalMoves.append(new_piece_position)
                else:
                    east_f = False
                if new_piece_position[0]=='A' or new_piece_position[0]=='H': #Check the edge of the board
                    east_f = False
            if west_f:
                pointer_west += 1
                new_piece_position =  chr(int(ord(column)) + pointer_west) + row    #Moving across a row , column changes and row is constant
                if new_piece_position not in board:
                    legalMoves.append(new_piece_position)
                else:
                    west_f = False
                if new_piece_position[0]=='A' or new_piece_position[0]=='H':
                    west_f = False
            if north_f:
                pointer_north += 1
                print('run')
                new_piece_position = column + str(pointer_north+ int(selectedPiece_position[1])) #Moving across a column , row changes and column is constant
                print(new_piece_position)
                if new_piece_position not in board:
                    legalMoves.append(new_piece_position)
                else:
                    north_f = False
                if new_piece_position[1]=='1' or new_piece_position[1]=='8':
                    north_f = False
            if south_f:
                pointer_south += 1
                print('run')
                new_piece_position = column + str(int(selectedPiece_position[1]) - pointer_south) #Moving across a column , row changes and column is constant
                print(new_piece_position)
                if new_piece_position not in board:
                    legalMoves.append(new_piece_position)
                else:
                    south_f = False
                if new_piece_position[1]=='1' or new_piece_position[1]=='8':
                    south_f = False
    return sorted(legalMoves)

print(legalMove(board , Piece , Piece_position))
        


         

    