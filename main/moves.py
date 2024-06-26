from typing import Union

def read_FEN(fen_str: str) -> tuple[str, dict]:
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
    return player_to_move, piece_position


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

from main.pieces import (Piece , Rook , Pawn , Bishop , Queen , Knight , King)

def generate_square(token: int) -> str:
    '''
    output:[square , 'Invalid']
    '''

    if token < 1 or token > 64:
        return 'Invalid'
    
    row = (token - 1) // 8
    col = (token - 1) % 8
    file_letter = chr(ord('A') + col)
    rank_number = row + 1
    return f"{file_letter}{rank_number}"


def token_generator(piece_position: str) -> Union[int, str]:
    '''
    output:[token , 'Invalid']
    '''

    char, row_number = piece_position
    row_number = int(row_number)
    multiplier = 10

    token = (ord(char) - 65) + ((row_number - 1)* multiplier) - 2*(row_number - 1) + 1

    if not 1 <= token <= 64:
        return 'Invalid'
    
    return token


def token_piece_position_table_gen(piece_position_table: dict[str, str]) -> dict[int, str]:
    table = {}

    for key, val in piece_position_table.items():
        table[token_generator(key)] = val

    return table

def get_current_player(turn_total: int) -> str:
    if turn_total % 2 == 0:
        return 'l'
    
    return 'd'

def get_piece_moves(piece_position_table: dict, selected_piece: str, selected_piece_position: str, turn_total: int, can_castle: dict) -> list:
    '''
    Returns pseudo-legal piece moves
    '''

    piece_identifier, colour = selected_piece

    token_piece_position_table = token_piece_position_table_gen(piece_position_table)
    token = token_generator(selected_piece_position)

    if piece_identifier == 'p':
        piece_type = Pawn(colour, token)
    elif piece_identifier == 'r':
        piece_type = Rook(colour, token)
    elif piece_identifier == 'b':
        piece_type = Bishop(colour, token)
    elif piece_identifier == 'q':
        piece_type = Queen(colour, token)
    elif piece_identifier == 'n':
        piece_type = Knight(colour, token)
    elif piece_identifier == 'k':
        piece_type = King(colour, token, can_castle)
    else:
        return []  # exception : Piece type not detected or is invalid
    piece_moves = piece_type.legal_moves_generator(token_piece_position_table)

    return sorted(piece_moves)


def update_board(piece_position_table: dict, selected_piece: str, selected_piece_position: str, target_position: str):
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


def in_check(piece_position_table: dict, turn_total: int, can_castle: dict) -> bool:
    '''
    Returns if current player is in check
    '''

    player = get_current_player(turn_total)
    enemy = 'ld'[player=='l']
    player_king_position = get_piece_position(piece_position_table, 'k'+player)

    for position, piece in piece_position_table.items():
        if piece[1] == enemy:  # get enemy pieces
            enemy_piece_legal_moves = get_piece_moves(piece_position_table, piece, position, turn_total+1, can_castle)

            if player_king_position in enemy_piece_legal_moves:
                return True

    return False


def is_checkmate(piece_position_table: dict, turn_total: int, can_castle: dict) -> bool:
    '''
    Returns if current player is checkmated
    '''

    if not in_check(piece_position_table, turn_total, can_castle):
        return False
    
    player = get_current_player(turn_total)

    for position, piece in piece_position_table.items():
        if piece[1] == player:  # get player pieces
            player_piece_legal_moves = get_piece_moves(piece_position_table, piece, position, turn_total, can_castle)

            for move in player_piece_legal_moves:
                temp_piece_position_table = piece_position_table.copy()
                update_board(temp_piece_position_table, piece, position, move)

                # check if move gets player out of check
                if not in_check(temp_piece_position_table, turn_total, can_castle):
                    return False
                
    return True


def legal_moves(piece_position_table: dict, selected_piece: str, selected_piece_position: str, turn_total: int, can_castle: dict) -> list:
    '''
    Returns the legal moves of selected piece | [] (if none)
    '''

    if selected_piece[1] != get_current_player(turn_total):
        return []

    legal_moves = []
    selected_piece_possible_moves = get_piece_moves(piece_position_table, selected_piece, selected_piece_position, turn_total, can_castle)
    
    # Handle Castling Edge Cases
    if selected_piece[0] == 'k' and can_castle[selected_piece[1]]:
        selected_piece_colour = selected_piece[1]
        enemy_piece_colour = 'ld'[selected_piece_colour == 'l']
        selected_piece_token = token_generator(selected_piece_position)

        king = King(selected_piece_colour, selected_piece_token, can_castle)
        
        # Prevent castling when in check
        if in_check(piece_position_table, turn_total, can_castle):
            selected_piece_possible_moves = list(filter(lambda move: not king.is_move_castle(move), selected_piece_possible_moves))

        # Prevent castling if an enemy piece targets squares in between king and rook
        elif any(map(king.is_move_castle, selected_piece_possible_moves)):
            for position, piece in piece_position_table.items():
                if piece[1] == enemy_piece_colour:
                    enemy_piece_target_squares = get_piece_moves(piece_position_table, piece, position, turn_total+1, can_castle)
                    
                    for castle_move in filter(king.is_move_castle, selected_piece_possible_moves):
                        adjacent_castle_squares = king.get_adjacent_castle_sqaures(castle_move)

                        if any(map(lambda x: x in adjacent_castle_squares, enemy_piece_target_squares)):
                            selected_piece_possible_moves.remove(castle_move)

                if not any(map(king.is_move_castle, selected_piece_possible_moves)):
                    break

    for move in selected_piece_possible_moves:
        # Simulate the move and see if it puts king in check
        temp_piece_position_table = piece_position_table.copy()
        update_board(temp_piece_position_table, selected_piece, selected_piece_position, move)

        if not in_check(temp_piece_position_table, turn_total, can_castle):
            legal_moves += [move]

    return legal_moves


if __name__ == '__main__':
    # Sample values , to be changes one js python communication is active
    _, piece_position_table = read_FEN('R6k/R7/8/8/8/8/8/8 b KQkq - 0 1')
    print(is_checkmate(piece_position_table, 1, {'l':'kq', 'd':'kq'}))
