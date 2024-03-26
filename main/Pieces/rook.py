from main.Pieces.piece import  Piece
import main.moves as moves

class Rook(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.directional_offset = [1 , -1 , 8 , -8]
        

    def legal_moves_generator(self, token_piece_position_table: dict) -> list:

        for offset in self.directional_offset:
            offset_multipler = 1
            while 1:
                token_pseudo_move = self.token + (offset * offset_multipler)
                token_pseudo_move_description = self.token_target_description(token_piece_position_table, token_pseudo_move , offset_val=offset)
                if token_pseudo_move_description == 'empty':
                    self.legal_moves.append(moves.generate_square(token_pseudo_move))
                elif token_pseudo_move_description == 'sameColour':
                    break
                elif token_pseudo_move_description == 'diffColour':
                    self.legal_moves.append(moves.generate_square(token_pseudo_move))
                    break
                else:
                    break
                offset_multipler += 1
                
        # Add legal move changes for rook, if required
        return self.legal_moves