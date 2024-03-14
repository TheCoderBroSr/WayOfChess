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

#A function which will determine the piece and output a list of all legal moves for the piece
def legal_moves(piece_position_table:dict , selected_piece:str , selected_piece_position:str) -> list:

    #Defining Row and Column of Piece

    column = selected_piece_position[0] #A-H
    row = selected_piece_position[1] #1-8
    legalMoves = []
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
                if new_piece_position[1]=='0' or new_piece_position[1]=='9' or new_piece_position[0]=='@' or new_piece_position[0]=='I':
                    east_f = False
                    continue
                if new_piece_position not in piece_position_table: #If there is no piece in the current position of pointer, that square won't exist in the piece position dictionary
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
                        south_f = False
                    else:
                        south_f = False
                

    if selected_piece[0] == 'b': #Defining rules of bishop ('b')
        '''
        To check all the moves of rook:
        -> Run 4 pointers in NW , NE , SE , SW
        -> If pointer reaches the edge of the board we terminate the loop
        -> We will iterate by 1 place in both directions specifies. F.E for NS direction from A8 will iterate to (A+1 ,8-1) = B7 ....
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
                        south_west_f = False
                    else:
                        south_west_f = False
        
    if selected_piece[0] == 'p':
        '''
        For pawn moving 2 or 1 position
        ->Check the row of the board to see if the pawn can move 2 spaces ahead. #Check 1
        ->If it can move 2 spaces ahead check if anything is blocking the path #Check 2

        ->if white pawn is on 5th row and opposing pawn moves to adjacent left or right positions en passent is activated.
        '''

        print(selected_piece , selected_piece_position)
        if (selected_piece[1] == 'l' and selected_piece_position[1] == '2'): #Check 1 for white

            

            new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) + 1) #1 Square ahead of the pawn
            new_piece_position_2 = selected_piece_position[0] + str(int(selected_piece_position[1]) + 2) #2 Square ahead of the pawn

            if new_piece_position_1 not in piece_position_table and new_piece_position_2 not in piece_position_table: #Check 2 for white
                legalMoves.extend([new_piece_position_1 , new_piece_position_2])
            elif new_piece_position_1 not in piece_position_table and new_piece_position_2 in piece_position_table:  
                legalMoves.append(new_piece_position_1)
            else:
                pass
        elif selected_piece[1] == 'd' and selected_piece_position[1] == '7': #Check 1 for black
            new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) - 1) #1 Square ahead of the pawn
            new_piece_position_2 = selected_piece_position[0] + str(int(selected_piece_position[1]) - 2) #2 Square ahead of the pawn

            if new_piece_position_1 not in piece_position_table and new_piece_position_2 not in piece_position_table: #Check 2 for white
                legalMoves.extend([new_piece_position_1 , new_piece_position_2])
            elif new_piece_position_1 not in piece_position_table and new_piece_position_2 in piece_position_table:  
                legalMoves.append(new_piece_position_1)
            else:
                pass
        else:
            if selected_piece[1] == 'd':   
                print('run')
                new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) - 1) #1 Square ahead of the pawn for black
                if new_piece_position_1 not in piece_position_table:
                    print(new_piece_position_1)
                    legalMoves.append(new_piece_position_1)
                else:
                    pass
            elif selected_piece[1] == 'l':   
                new_piece_position_1 = selected_piece_position[0] + str(int(selected_piece_position[1]) + 1) #1 Square ahead of the pawn for white
                if new_piece_position_1 not in piece_position_table:
                    legalMoves.append(new_piece_position_1)
                else:
                    pass
        '''
        To implement capture we just thave to check the top right position and top left and if it has a piece it will be a legal move
        '''
        if selected_piece[1] == 'l': #for white
            new_piece_position_r = (chr(int(ord(selected_piece_position[0])) + 1) + str(int(selected_piece_position[1]) + 1)) #top right
            new_piece_position_l = (chr(int(ord(selected_piece_position[0])) - 1) + str(int(selected_piece_position[1]) + 1)) #top left
            if new_piece_position_r in piece_position_table:
                if piece_position_table[new_piece_position_r][1] != selected_piece[1]:
                    legalMoves.append(new_piece_position_r)
            if new_piece_position_l in piece_position_table:
                if piece_position_table[new_piece_position_l][1] != selected_piece[1]:
                    legalMoves.append(new_piece_position_l)

        elif selected_piece[1] == "d": #for black
            new_piece_position_r = (chr(int(ord(selected_piece_position[0])) + 1) + str(int(selected_piece_position[1]) - 1)) #bottom right
            new_piece_position_l = (chr(int(ord(selected_piece_position[0])) - 1) + str(int(selected_piece_position[1]) - 1)) #bottom left
            if new_piece_position_r in piece_position_table:
                if piece_position_table[new_piece_position_r][1] != selected_piece[1]:
                    legalMoves.append(new_piece_position_r)
            if new_piece_position_l in piece_position_table:
                if piece_position_table[new_piece_position_l][1] != selected_piece[1]:
                    legalMoves.append(new_piece_position_l)
        
        '''if selected_piece[1] == 'l' and selected_piece_position[1] == '8':
            legalMoves.append(f"promotion/{selected_piece}/{selected_piece_position}")
        elif selected_piece[1] == 'd' and selected_piece_position[1] == '1':
            legalMoves.append(f"promotion/{selected_piece}/{selected_piece_position}")'''
        
                
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
            print(pos)
            if pos in piece_position_table:
                if piece_position_table[pos][1] != selected_piece[1]:
                   legalMoves.append(pos)
            else:
                if int(ord(pos[0])) >= 65 and int(ord(pos[0])) <= 72 and pos[1] != '-' and int(pos[1]) >= 1 and int(pos[1]) <= 8:
                    legalMoves.append(pos)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
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
                    legalMoves.append(new_piece_position)
                else:
                    if piece_position_table[new_piece_position][1] != selected_piece[1]: #Checks if the new piece positions's piece is not the same color as the originial piece (2 pieces of the same colour cannot capture each other)
                        legalMoves.append(new_piece_position)
                        south_west_f = False
                    else:
                        south_west_f = False
        
    return sorted(legalMoves)

if __name__ == '__main__':
#Sample values , to be changes one js python communication is active
    piece_position_table = read_FEN('Br1q1b2/p1p1pk2/1p1p2pp/3n1p2/3n2P1/1PP1P2r/P4K2/1N2QBN1 w KQkq - 0 1')
    selected_piece = 'bl'
    selected_piece_position = 'F1'

    print(legal_moves(piece_position_table, selected_piece , selected_piece_position))
