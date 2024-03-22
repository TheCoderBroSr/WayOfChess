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
def token_generator(board_position : str) -> int:
    char , row_number = board_position
    row_number = int(row_number)
    multuplier = 10
    token = (ord(char) - 65) + ((row_number- 1) * multuplier) - 2*(row_number - 1) + 1
    return token

def generate_square(token: int) -> str:
    if 1 <= token <= 64:
        row = (token - 1) // 8
        col = (token - 1) % 8
        file_letter = chr(ord('A') + col)
        rank_number = row +1
        return f"{file_letter}{rank_number}"
            

def token_piece_position_table_gen(piece_position_table):
    table = {}
    for key , val in piece_position_table.items():
        table[token_generator(key)] = val
    return table

def get_piece_moves(piece_position_table:dict , selected_piece:str , selected_piece_position:str) -> list:
    '''
    Returns all possible piece moves excluding friendly piece captures
    '''

    class pieces:
        class bishop:
            directionalOffset = [9 , -9 , -7 , 7]

    #Defining Row and Column of Piece
    piece , piece_colour = selected_piece
    column = selected_piece_position[0] #A-H
    row = selected_piece_position[1] #1-8
    piece_moves = []
    token_piece_position_table = token_piece_position_table_gen(piece_position_table)

    def square_check(new_piece_position : str) -> str:
        '''
        For each piece we will run a certain pointer in a certain direction with certain rules. Each time a pointer changes its position
        in the chess board there will be 4 possible cases
        -> The square is outside the board. #case 1 -> 'OB' (Out of bounds)

        There is a piece on the square
            -> There is a piece on the square of oppposite colour. #case 2 -> 'oppositeColor'
            -> There is a piece on the square of the same colour. #check 3 -> 'sameColor'
        -> There is no piece on that square. #check 4 -> noPiece
        '''
        if  'A' <= new_piece_position[0] <= 'H'   and '1' <= new_piece_position[1] <= '8': 
            if new_piece_position in piece_position_table:
                if piece_position_table[new_piece_position][1] == selected_piece[1]:
                    return 'sameColor' #case 3
                else:
                    return 'oppositeColor' #case 2
            else:
                return 'noPiece' #case 4
        else:
            return 'OB' #Case 1
            
                
                    

    if selected_piece[0] == 'r': #Defining Rules for rook ('r')
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

        pointer_east = pointer_west = pointer_north = pointer_south = 0 #Initial Pointer Position
        east_f = west_f = north_f = south_f = True

        while east_f or west_f or north_f or south_f:
            if east_f:
                pointer_east += 1 #Moving 1 step left
                new_piece_position =  chr(int(ord(column)) - pointer_east) + row #Moving across a row , column changes and row is constant
                if square_check(new_piece_position) == 'OB':
                    east_f = False
                    continue
                if square_check(new_piece_position) == 'noPiece': #If there is no piece in the current position of pointer, that square won't exist in the piece position dictionary
                    piece_moves.append(new_piece_position)
                else:
                    if square_check(new_piece_position) == 'oppositeColor': #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        east_f = False
                    elif square_check(new_piece_position) == 'sameColor':
                        east_f = False
                    else:
                        return 'pawn edge case error'
            if west_f:
                pointer_west += 1
                new_piece_position =  chr(int(ord(column)) + pointer_west) + row #Moving across a row , column changes and row is constant
                if square_check(new_piece_position) == 'OB':
                    west_f = False
                    continue
                if square_check(new_piece_position) == 'noPiece':
                    piece_moves.append(new_piece_position)
                else:
                    if square_check(new_piece_position) == 'oppositeColor': #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        west_f = False
                    elif square_check(new_piece_position) == 'sameColor':
                        west_f = False
                    else:
                        return 'pawn edge case error'
            if north_f:
                pointer_north += 1
                new_piece_position = column + str(pointer_north+ int(selected_piece_position[1])) #Moving across a column , row changes and column is constant
                if square_check(new_piece_position) == 'OB':
                    north_f = False
                    continue
                if square_check(new_piece_position) == 'noPiece':
                    piece_moves.append(new_piece_position)
                else:
                    if square_check(new_piece_position) == 'oppositeColor': #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        north_f = False
                    elif square_check(new_piece_position) == 'sameColor':
                        north_f = False
                    else:
                        return 'pawn edge case error'
                
            if south_f:
                pointer_south += 1
                new_piece_position = column + str(int(selected_piece_position[1]) - pointer_south) #Moving across a column , row changes and column is constant
                if square_check(new_piece_position) == 'OB':
                    south_f = False
                    continue
                if square_check(new_piece_position) == 'noPiece':
                    piece_moves.append(new_piece_position)
                else:
                    if square_check(new_piece_position) == 'oppositeColor': #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        south_f = False
                    elif square_check(new_piece_position) == 'sameColor':
                        south_f = False
                    else:
                        return 'pawn edge case error'
    counter = 0
    if selected_piece[0] == 'b': #Defining rules of bishop ('b')
        '''
        To check all the moves of rook:
        -> Run 4 pointers in NW , NE , SE , SW
        -> If pointer reaches the edge of the board we terminate the loop
        -> We will iterate by 1 place in both directions specifies. F.E for NS direction from A8 will iterate to (A+1 ,8-1) = B7 ....
        '''
        offset_multiplier = 1
        for directional_offset in pieces.bishop.directionalOffset:
            while 1:
                new_piece_square = token_generator(selected_piece_position) + (directional_offset * offset_multiplier)
                print(new_piece_square)
                if new_piece_square in list(token_piece_position_table.keys()):
                    if token_piece_position_table[new_piece_square][1] == piece_colour:
                        break
                    else:
                        piece_moves.append(generate_square(new_piece_square))
                        offset_multiplier += 1
                else:
                    if 1 <= new_piece_square <= 64:
                        piece_moves.append(generate_square(new_piece_square))
                        offset_multiplier += 1
                    else:
                        break
            print(piece_moves)
        '''
        north_west_f = north_east_f = south_east_f = south_west_f = True
        pointer_north_west_f = pointer_north_east_f = pointer_south_east_f = pointer_south_west_f = 0

        while north_east_f or north_west_f or south_east_f or south_west_f: 
            if north_east_f:
                pointer_north_east_f += 1
                new_piece_position = chr(int((ord(column)) + pointer_north_east_f)) + str((int(row) + pointer_north_east_f)) #To move in NE direction our pointer moves +1 position in both column and row
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I': #This code checks that if the piece has moved to a position outside the respective directional loop will stop
                    north_east_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        north_east_f = False
                    else:
                        north_east_f = False
            
            if north_west_f:
                pointer_north_west_f += 1
                new_piece_position = chr(int((ord(column)) - pointer_north_west_f)) + str((int(row) + pointer_north_west_f)) #To move in NW direction our pointer moves -1 position in column and +1 in row
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    north_west_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        north_west_f = False
                    else:
                        north_west_f = False
            
            if south_east_f:
                pointer_south_east_f += 1
                new_piece_position = chr(int((ord(column)) - pointer_south_east_f)) + str((int(row) - pointer_south_east_f)) #To move in SE direction our pointer moves +1 position in column and -1 in row 
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    south_east_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        south_east_f = False
                    else:
                        south_east_f = False
            
            if south_west_f:
                pointer_south_west_f += 1
                new_piece_position = chr(int((ord(column)) + pointer_south_west_f)) + str((int(row) - pointer_south_west_f)) #To move in SW direction our pointer moves -1 position in column and -1 in row 
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    south_west_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        south_west_f = False
                    else:
                        south_west_f = False
            '''
        
    if selected_piece[0] == 'p':
        '''
        For pawn moving 2 or 1 position
        ->Check the row of the board to see if the pawn can move 2 spaces ahead. #Check 1
        ->If it can move 2 spaces ahead check if anything is blocking the path #Check 2

        ->if white pawn is on 5th row and opposing pawn moves to adjacent left or right positions en passent is activated.
        '''

        if (selected_piece[1] == 'l' and selected_piece_position[1] == '2'): #Check 1 for white
            
            new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) + 1) #1 Square ahead of the pawn
            new_piece_position_2 = selected_piece_position[0] + str(int(selected_piece_position[1]) + 2) #2 Square ahead of the pawn

            if square_check(new_piece_position_1) == 'noPiece' and square_check(new_piece_position_2) == 'noPiece': #Check 2 for white
                piece_moves.extend([new_piece_position_1 , new_piece_position_2])
            elif square_check(new_piece_position_1) == 'noPiece' and new_piece_position_2 in piece_position_table:  
                piece_moves.append(new_piece_position_1)
            else:
                pass
        elif selected_piece[1] == 'd' and selected_piece_position[1] == '7': #Check 1 for black
            new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) - 1) #1 Square ahead of the pawn
            new_piece_position_2 = selected_piece_position[0] + str(int(selected_piece_position[1]) - 2) #2 Square ahead of the pawn

            if square_check(new_piece_position_1) == 'noPiece' and square_check(new_piece_position_2) == 'noPiece': #Check 2 for white
                piece_moves.extend([new_piece_position_1 , new_piece_position_2])
            elif square_check(new_piece_position_1) == 'noPiece' and new_piece_position_2 in piece_position_table:  
                piece_moves.append(new_piece_position_1)
            else:
                pass
        else:
            if selected_piece[1] == 'd':   
                new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) - 1) #1 Square ahead of the pawn for black
                if square_check(new_piece_position_1) == 'noPiece':
                    piece_moves.append(new_piece_position_1)
                else:
                    pass
            elif selected_piece[1] == 'l':   
                new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) + 1) #1 Square ahead of the pawn for white
                if square_check(new_piece_position_1) == 'noPiece':
                    piece_moves.append(new_piece_position_1)
                else:
                    pass
        '''
        To implement capture we just thave to check the top right position and top left and if it has a piece it will be a legal move
        '''
        if selected_piece[1] == 'l': #for white
            new_piece_position_r = (chr(int(ord(selected_piece_position[0])) + 1) + str(int(selected_piece_position[1]) + 1)) #top right
            new_piece_position_l = (chr(int(ord(selected_piece_position[0])) - 1) + str(int(selected_piece_position[1]) + 1)) #top left
            if square_check(new_piece_position_r) == 'oppositeColor':
                piece_moves.append(new_piece_position_r)
            if square_check(new_piece_position_l) == 'oppositeColor':
                    piece_moves.append(new_piece_position_l)

        elif selected_piece[1] == "d": #for black
            new_piece_position_r = (chr(int(ord(selected_piece_position[0])) + 1) + str(int(selected_piece_position[1]) - 1)) #bottom right
            new_piece_position_l = (chr(int(ord(selected_piece_position[0])) - 1) + str(int(selected_piece_position[1]) - 1)) #bottom left
            if square_check(new_piece_position_r) == 'oppositeColor':
                piece_moves.append(new_piece_position_r)
            if square_check(new_piece_position_l) == 'oppositeColor':
                    piece_moves.append(new_piece_position_l)
        
        '''if selected_piece[1] == 'l' and selected_piece_position[1] == '8':
            piece_moves.append(f"promotion/{selected_piece}/{selected_piece_position}")
        elif selected_piece[1] == 'd' and selected_piece_position[1] == '1':
            piece_moves.append(f"promotion/{selected_piece}/{selected_piece_position}")'''
        
                
    if selected_piece[0] == 'n':

        'Knight can move in 8 directions'
        new_piece_position_2U_1R = (chr(int(ord(selected_piece_position[0])) + 1) + str(int(selected_piece_position[1]) + 2)) #Up 2 spaces and 1 right
        new_piece_position_2U_1L = (chr(int(ord(selected_piece_position[0])) - 1) + str(int(selected_piece_position[1]) + 2)) #
        new_piece_position_2D_1R = (chr(int(ord(selected_piece_position[0])) + 1) + str(int(selected_piece_position[1]) - 2)) #
        new_piece_position_2D_1L = (chr(int(ord(selected_piece_position[0])) - 1) + str(int(selected_piece_position[1]) - 2)) #
        new_piece_position_1U_2R = (chr(int(ord(selected_piece_position[0])) + 2) + str(int(selected_piece_position[1]) + 1)) #
        new_piece_position_1U_2L = (chr(int(ord(selected_piece_position[0])) - 2) + str(int(selected_piece_position[1]) + 1)) #
        new_piece_position_1D_2R = (chr(int(ord(selected_piece_position[0])) + 2) + str(int(selected_piece_position[1]) - 1)) #
        new_piece_position_1D_2L = (chr(int(ord(selected_piece_position[0])) - 2) + str(int(selected_piece_position[1]) - 1)) #

        def knight_check(pos):
            if pos in piece_position_table:
                if piece_position_table[pos][1] != selected_piece[1]:
                   if int(ord(pos[0])) >= 65 and int(ord(pos[0])) <= 72 and pos[1] != '-' and int(pos[1]) >= 1 and int(pos[1]) <= 8:
                    piece_moves.append(pos)
            else:
                if int(ord(pos[0])) >= 65 and int(ord(pos[0])) <= 72 and pos[1] != '-' and int(pos[1:]) >= 1 and int(pos[1:]) <= 8:
                    piece_moves.append(pos)
        #Running check function for all 8 directions
        knight_check(new_piece_position_2U_1R)
        knight_check(new_piece_position_2U_1L)
        knight_check(new_piece_position_2D_1R)
        knight_check(new_piece_position_2D_1L)
        knight_check(new_piece_position_1U_2R)
        knight_check(new_piece_position_1U_2L)
        knight_check(new_piece_position_1D_2R)
        knight_check(new_piece_position_1D_2L)

    if selected_piece[0] == 'q':
        pointer_east = pointer_west = pointer_north = pointer_south = 0 #Initial Pointer Position
        east_f = west_f = north_f = south_f = True
        while east_f or west_f or north_f or south_f:
            if east_f:
                pointer_east += 1 #Moving 1 step left
                new_piece_position =  chr(int(ord(column)) - pointer_east) + row #Moving across a row , column changes and row is constant
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    east_f = False
                    continue
                if new_piece_position not in piece_position_table: #If there is no piece in the current position of pointer, that square won't exist in the piece position dictionary
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        east_f = False
                    else:
                        east_f = False
            if west_f:
                pointer_west += 1
                new_piece_position =  chr(int(ord(column)) + pointer_west) + row    #Moving across a row , column changes and row is constant
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    west_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        west_f = False
                    else:
                        west_f = False
            if north_f:
                pointer_north += 1
                new_piece_position = column + str(pointer_north+ int(selected_piece_position[1])) #Moving across a column , row changes and column is constant
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    north_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        north_f = False
                    else:
                        north_f = False
                
            if south_f:
                pointer_south += 1
                new_piece_position = column + str(int(selected_piece_position[1]) - pointer_south) #Moving across a column , row changes and column is constant
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    south_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        south_f = False
                    else:
                        south_f = False

        north_west_f = north_east_f = south_east_f = south_west_f = True
        pointer_north_west_f = pointer_north_east_f = pointer_south_east_f = pointer_south_west_f = 0

        while north_east_f or north_west_f or south_east_f or south_west_f: 
            if north_east_f:
                pointer_north_east_f += 1
                new_piece_position = chr(int((ord(column)) + pointer_north_east_f)) + str((int(row) + pointer_north_east_f)) #To move in NE direction our pointer moves +1 position in both column and row
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I': #This code checks that if the piece has moved to a position outside the respective directional loop will stop
                    north_east_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        north_east_f = False
                    else:
                        north_east_f = False
            
            if north_west_f:
                pointer_north_west_f += 1
                new_piece_position = chr(int((ord(column)) - pointer_north_west_f)) + str((int(row) + pointer_north_west_f)) #To move in NW direction our pointer moves -1 position in column and +1 in row
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    north_west_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        north_west_f = False
                    else:
                        north_west_f = False
            
            if south_east_f:
                pointer_south_east_f += 1
                new_piece_position = chr(int((ord(column)) - pointer_south_east_f)) + str((int(row) - pointer_south_east_f)) #To move in SE direction our pointer moves +1 position in column and -1 in row 
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    south_east_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        south_east_f = False
                    else:
                        south_east_f = False
            
            if south_west_f:
                pointer_south_west_f += 1
                new_piece_position = chr(int((ord(column)) + pointer_south_west_f)) + str((int(row) - pointer_south_west_f)) #To move in SW direction our pointer moves -1 position in column and -1 in row 
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    south_west_f = False
                    continue
                if new_piece_position not in piece_position_table:
                    piece_moves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        piece_moves.append(new_piece_position)
                        south_west_f = False
                    else:
                        south_west_f = False
    
    if selected_piece[0] == 'k':
        #8 Pointers for each direction the king can move
        
        pointer_N = chr(ord(selected_piece_position[0]) + 0) + str(int(selected_piece_position[1]) + 1)
        pointer_NE = chr(ord(selected_piece_position[0]) + 1) + str(int(selected_piece_position[1]) + 1)
        pointer_E = chr(ord(selected_piece_position[0]) + 1) + str(int(selected_piece_position[1]) + 0)
        pointer_SE = chr(ord(selected_piece_position[0]) + 1) + str(int(selected_piece_position[1]) - 1)
        pointer_S = chr(ord(selected_piece_position[0]) + 0) + str(int(selected_piece_position[1]) - 1)
        pointer_SW = chr(ord(selected_piece_position[0]) -1) + str(int(selected_piece_position[1]) - 1)
        pointer_W = chr(ord(selected_piece_position[0]) - 1) + str(int(selected_piece_position[1]) + 0)
        pointer_NW = chr(ord(selected_piece_position[0]) -1) + str(int(selected_piece_position[1]) + 1)
        
        directions = [pointer_N , pointer_NE , pointer_E , pointer_SE , pointer_S , pointer_SW , pointer_W , pointer_NW]

        for i in directions:
            if square_check(i) == 'oppositeColor':  
                piece_moves.append(i)
            if square_check(i) == 'noPiece':
                piece_moves.append(i)
        #Castling
                


    return sorted(piece_moves)



def update_board(piece_position_table:dict, selected_piece:str, selected_piece_position:str, target_position:str):
    '''
    Places selected piece at target square
    Removes selected piece from initial square
    '''

    piece_position_table[target_position] = selected_piece
    del piece_position_table[selected_piece_position]

def get_piece_position(piece_position_table, search_piece):
    '''
    piece -> piece_type + piece_colour eg. kl, nd etc

    Returns the first piece found
    '''

    for position, piece in piece_position_table.items():
        if piece == search_piece:
            return position

def in_check(piece_position_table:dict, player:str) -> bool:
    if player == 'l':
        enemy = 'd'
    else:
        enemy = 'l'

    player_king_position = get_piece_position(piece_position_table, 'k'+player)

    for position, piece in piece_position_table.items():
        if piece[1] == enemy: # get enemy pieces 
            enemy_piece_legal_moves = get_piece_moves(piece_position_table, piece, position)

            if player_king_position in enemy_piece_legal_moves:
                return True
            
    return False

def legal_moves(piece_position_table:dict , selected_piece:str , selected_piece_position:str) -> list:
    selected_piece_colour = selected_piece[1]
    legal_moves = []
    
    selected_piece_possible_moves = get_piece_moves(piece_position_table, selected_piece, selected_piece_position)

    for move in selected_piece_possible_moves:
        # Simulate the move and see if it puts king in check
        temp_piece_position_table = piece_position_table.copy()
        update_board(temp_piece_position_table, selected_piece, selected_piece_position, move)

        if not in_check(temp_piece_position_table, selected_piece_colour):
            legal_moves += [move]

    return legal_moves

if __name__ == '__main__':
#Sample values , to be changes one js python communication is active
    piece_position_table = read_FEN('8/8/2k5/8/8/8/8/1KR5 w KQkq - 0 1')
    selected_piece = 'kd'

    player = selected_piece[1]

    print(in_check(piece_position_table, player))
