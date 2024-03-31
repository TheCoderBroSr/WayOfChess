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

    def legal_moves_generator_slidingPieces(self , token_piece_position_table : dict):
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
    
    def legal_moves_generator_knight(self , token_piece_position_table : dict):
        for offset in self.directional_offset:
            target_position = self.token + offset
            token_target_description = self.token_target_description(token_piece_position_table , target_position , offset_val=offset)
            if token_target_description == 'empty' or token_target_description == 'diffColour':
                self.legal_moves.append(moves.generate_square(target_position))

    def legal_moves_generator_king(self , token_piece_position_table : dict):
        for offset in self.directional_offset:
            target_position = self.token + offset
            token_target_description = token_target_description = self.token_target_description(token_piece_position_table , target_position , offset_val=offset)
            if token_target_description == 'empty' or token_target_description == 'diffColour':
                self.legal_moves.append(moves.generate_square(target_position))

    def turn(self ,turn_total):
        if turn_total % 2 == 1:
            return 'd'
        else:
            return 'l'
                
class Rook(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.directional_offset = [1 , -1 , 8 , -8]

    def legal_moves_generator(self, token_piece_position_table: dict) -> list:
        super(self.__class__, self).legal_moves_generator_slidingPieces(token_piece_position_table)

        return self.legal_moves
    
class Bishop(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.directional_offset = [9 , -9 , 7 , -7]

    def legal_moves_generator(self, token_piece_position_table: dict) -> list:
        super(self.__class__, self).legal_moves_generator_slidingPieces(token_piece_position_table)

        return self.legal_moves

class Queen(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.directional_offset = [8 , 9 , 7 , 1 , -9 , -8 , -7 , -1]

    def legal_moves_generator(self, token_piece_position_table: dict) -> list:
        super(self.__class__, self).legal_moves_generator_slidingPieces(token_piece_position_table)

        return self.legal_moves



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


    def legal_moves_generator(self, token_piece_position_table: dict) -> list:
        # Add all non-captures to legal_moves


        super(self.__class__, self).legal_moves_generator_pawn(token_piece_position_table) 
        # Call legal_moves_generator method from the parent class i.e. Piece

        self.capture = True

        if self.colour == 'l':
            self.directional_offset = self.general_directional_offset[4:6]
        else:
            self.directional_offset = self.general_directional_offset[6:]

        # Add all captures to legal_moves
        super(self.__class__, self).legal_moves_generator_pawn(token_piece_position_table) 

        self.capture = False

        # Handle special legal moves here, for instance en passant

        return self.legal_moves
    
class Knight(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.directional_offset = [17 , 15 , -17 , -15 , 10 , -10 , 6 , -6]

    def legal_moves_generator(self, token_piece_position_table: dict):
        super(self.__class__, self).legal_moves_generator_knight(token_piece_position_table) 
        
        return self.legal_moves

class King(Piece):
    def __init__(self, colour, token) -> None:
        super().__init__(colour, token)
        self.directional_offset = [8 , 9 , 1 , -9 , -8 , -7 , 7 , -1]

    def legal_moves_generator(self, token_piece_position_table: dict):
        super(self.__class__, self).legal_moves_generator_king(token_piece_position_table) 
        
        return self.legal_moves  