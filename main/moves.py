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

'''
NOTE:
The Piece Class (and by extension all the children class like rook, pawn etc) will be representing the selected piece
'''

from main.pieces import (Piece , Rook , Pawn , Bishop , Queen , Knight)

def generate_square(token: int) -> str:
    '''
    output:[square , 'Invalid']
    '''
    if 1 <= token <= 64:
        row = (token - 1) // 8
        col = (token - 1) % 8
        file_letter = chr(ord('A') + col)
        rank_number = row +1
        return f"{file_letter}{rank_number}"
    else:
        return 'Invalid'

def token_generator(piece_position: str) -> int:
    '''
    output:[token , 'Invalid']
    '''
    char, row_number = piece_position
    row_number = int(row_number)
    multuplier = 10
    token = (ord(char) - 65) + ((row_number- 1) * multuplier) - 2*(row_number - 1) + 1
    if not 1 <= token <= 64:
        return 'Invalid'
    return token
    

def token_piece_position_table_gen(piece_position_table):
    table = {}
    for key, val in piece_position_table.items():
        table[token_generator(key)] = val
    return table

def get_piece_moves(piece_position_table:dict , selected_piece:str , selected_piece_position:str) -> list:
    '''
    Returns pseudo-legal piece moves
    '''

    piece_identifier, colour = selected_piece

    token_piece_position_table = token_piece_position_table_gen(piece_position_table)
    token = token_selected_piece_position = token_generator(selected_piece_position)
    
    piece = Piece(colour , token_piece_position_table)
    if piece_identifier == 'p':
        piece_type = Pawn(colour , token)
    elif piece_identifier == 'r':
        piece_type = Rook(colour , token)
    elif piece_identifier == 'b':
        piece_type = Bishop(colour , token)
    elif piece_identifier == 'q':
        piece_type = Queen(colour , token)
    elif piece_identifier == 'n':
        piece_type = Knight(colour , token)
    else:
        return [] #exception : Piece type not detected or is invalid
    piece_moves = piece_type.legal_moves_generator(token_piece_position_table)

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
    
    '''selected_piece_possible_moves = get_piece_moves(piece_position_table, selected_piece, selected_piece_position)

    for move in selected_piece_possible_moves:
        # Simulate the move and see if it puts king in check
        temp_piece_position_table = piece_position_table.copy()
        update_board(temp_piece_position_table, selected_piece, selected_piece_position, move)

        if not in_check(temp_piece_position_table, selected_piece_colour):
            legal_moves += [move]

    return legal_moves'''
    legal_moves = get_piece_moves(piece_position_table,selected_piece , selected_piece_position)
    return legal_moves

if __name__ == '__main__':
#Sample values , to be changes one js python communication is active
    piece_position_table = read_FEN('8/p7/1Rk5/8/8/8/8/1KR5 w KQkq - 0 1')
    selected_piece = 'pd'
    selected_piece_position = 'A7'

    selected_piece_moves = get_piece_moves(piece_position_table, selected_piece, selected_piece_position)

    print(selected_piece_moves)