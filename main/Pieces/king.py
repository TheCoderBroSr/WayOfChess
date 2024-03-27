from main.Pieces.piece import  Piece
import main.moves as moves

class King(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.directional_offset = [8 , 9 , 1 , -9 , -8 , -7 , -1 , 7]
    
    def legal_moves_generator(self, token_piece_position_table: dict):
        for offset in self.directional_offset:
            target_position = self.token + offset
            token_target_description = self.token_target_description(token_piece_position_table , target_position , offset_val=offset)
            if token_target_description == 'empty' or token_target_description == 'diffColour':
                self.legal_moves.append(moves.generate_square(target_position))
            else:
                continue
        return self.legal_moves
