import main.moves as moves

class Piece:

    def __init__(self, colour, token) -> None:
        self.directional_offset = None
        self.capture = False
        self.colour = colour
        self.token = token
        self.legal_moves = []

    def isvalidToken(self , token : int) -> bool:
        if 1 <= token <=64 :
            return True
        else:
            return False

    def token_target_description(self, token_piece_position_table: dict, token_target_position: int , offset_val = 0) -> str:
        '''
        Return accordingly if target token in token_piece_position_table is empty or has a piece
        output: ['sameColour' , 'doffColour' , 'empty' , 'outOfBounds']
        '''
        #Capturable just not by a pawn

        def piece_check() -> str:
            if token_target_position in token_piece_position_table:
                if self.colour == token_piece_position_table[token_target_position][1]:
                    return 'sameColour'
                else:
                    return 'diffColour'
            else:
                return 'None'

        if self.isvalidToken(token_target_position): 
            if abs(offset_val) == 1:
                column,row = moves.generate_square(self.token)
                if row == moves.generate_square(token_target_position)[1]:
                    if piece_check() != 'None':
                        return piece_check()
                    else:
                        return 'empty'
                else:
                    return 'outOfBounds'
            elif abs(offset_val) == 8 :
                    if piece_check() != 'None':
                        return piece_check()
                    else:
                        return 'empty'
            elif abs(offset_val) == 9 or abs(offset_val) == 7 and self.isvalidToken(token_target_position):
                column,row = moves.generate_square(self.token)
                if offset_val == 9 or offset_val == -7:
                    if moves.generate_square(token_target_position)[0] > column:
                        if piece_check() != 'None':
                            return piece_check()
                        else:
                            return 'empty'
                    else:
                        return 'outOfBounds'
                if abs(offset_val) == 7 or offset_val == -9:
                    if moves.generate_square(token_target_position)[0] < column:
                        if piece_check() != 'None':
                            return piece_check()
                        else:
                            return 'empty'
                    else:
                        return 'outOfBounds'
            else: #Knight':
                column , row = moves.generate_square(self.token)
                target_column , target_row = moves.generate_square(token_target_position)
                if abs(offset_val) == 10 or abs(offset_val) == 6:
                    if abs(int(target_row) - int(row)) != 1:
                        return 'outOfBounds'
                elif abs(offset_val) == 17 or abs(offset_val) == 15:
                    if abs(int(target_row) - int(row)) != 2:
                        return 'outOfBounds'
                    
                if piece_check() != 'None':
                    return piece_check()
                else:
                    return 'empty'

        else:
            return 'outOfBounds'
            

    





            