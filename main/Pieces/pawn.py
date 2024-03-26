from main.Pieces.piece import  Piece
import main.moves as moves

class Pawn(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.general_directional_offset = [8 , 16 , -8 , -16 , 9 , 7 , -9 , -7]

        if 9 <= self.token <= 16 and self.colour == 'l':
            self.directional_offset = self.general_directional_offset[:2]
        elif 49 <= self.token <= 56 and self.colour == 'd':
            self.directional_offset = self.general_directional_offset[2:4]
        elif self.colour == 'd':
            self.directional_offset = [self.general_directional_offset[2]]
        elif self.colour == 'l':
            self.directional_offset = [self.general_directional_offset[0]]

    def legal_moves_generator_pawn(self, token_piece_position_table: dict):
        '''
        General legal moves generator for pawn pieces
        Updates self.legal_moves
        '''
        for offset in self.directional_offset:
            token_pseudo_move = self.token + offset
            
            token_pseudo_move_description = self.token_target_description(token_piece_position_table, token_pseudo_move , offset_val = offset)
            if token_pseudo_move_description == 'empty' and self.capture == False:
                self.legal_moves.append(moves.generate_square(token_pseudo_move))           
            elif token_pseudo_move_description == 'diffColour' and self.capture == True:
                self.legal_moves.append(moves.generate_square(token_pseudo_move))
            elif self.capture == False:
                break

    def legal_moves_generator(self, token_piece_position_table: dict) -> list:
        # Add all non-captures to legal_moves


        self.legal_moves_generator_pawn(token_piece_position_table) 
        # Call legal_moves_generator method from the parent class i.e. Piece

        self.capture = True

        if self.colour == 'l':
            self.directional_offset = self.general_directional_offset[4:6]
        else:
            self.directional_offset = self.general_directional_offset[6:]

        # Add all captures to legal_moves
        self.legal_moves_generator_pawn(token_piece_position_table) 

        self.capture = False

        # Handle special legal moves here, for instance en passant

        return self.legal_moves
    