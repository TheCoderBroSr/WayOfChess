from . import moves
from . import pieces
import os
import json

from flask import ( 
    Flask, render_template, request, session, url_for, flash, jsonify , sessions    
)

def create_app(test_config=None):
    # create and configure the app
    global turn_total
    turn_total = 0

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'main.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    APP_URL = 'http://127.0.0.1:5000'
    START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' # FEN str for starting position

    @app.route('/', methods=('GET', 'POST'))
    def index():

        session['can_castle_l'] = [1 , 1]
        #1st element represent queen side castle and 2nd element represent king side castle
        #1 -> True , can castle ; 0 -> False , can not castle

        if 'piece_position_table' not in session:
            session['piece_position_table'] = moves.read_FEN(START_POSITION)
            global turn_total
            turn_total = 0

        if 'app_url' not in session:
            session['app_url'] = APP_URL

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('index.html')        

    @app.route('/dev', methods=('GET', 'POST'))
    def dev():
        '''
        k -> king
        q -> queen
        r -> rook
        n -> knight
        b -> bishop
        p -> pawn

        l -> light(white)
        d -> dark(black)
        '''
        global turn_total

        session['can_castle_l'] = [1 , 1]
        #1st element represent queen side castle and 2nd element represent king side castle
        #1 -> True , can castle ; 0 -> False , can not castle

        if 'piece_position_table' not in session:
            session['piece_position_table'] = moves.read_FEN(START_POSITION)
            turn_total = 0

        if 'app_url' not in session:
            session['app_url'] = APP_URL

        if request.method == "POST" and 'reset' in request.form:
            session['piece_position_table'] = moves.read_FEN(START_POSITION)
            turn_total = 0
            

        elif request.method == "POST" and 'set' in request.form:
            custom_position = request.form['fen_position']

            # Implement valid FEN string check
            try:
                session['piece_position_table'] = moves.read_FEN(custom_position)
            except:
                flash('Invalid FEN string')

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('dev.html')

    @app.route('/process_move', methods=['POST'])
    def process_move():
        '''
        Custom HTTP Status Codes
        210 -> Successfully received selected_piece info
        211 -> Legal piece move made
        221 -> Illegal piece move made
        231 -> CheckMate
        '''
        global turn_total
        piece_data = request.json

        if 'selected_piece' not in session:
            session['selected_piece'] = None
        
        if 'selected_piece_position' not in session:
            session['selected_piece_position'] = None

        piece_position_table = session['piece_position_table']

        if piece_data['data'] == 'initial_data':
            session['selected_piece'] = piece_data['selected_piece']
            session['selected_piece_position'] = piece_data['selected_piece_position']         
            legal_moves = moves.legal_moves(session['piece_position_table'], session['selected_piece'], session['selected_piece_position']  ,turn_total, session['can_castle_l'] )
            response_data = {'legal_moves': legal_moves}
            
            status_code = 210

            return jsonify(response_data), status_code
        
        if piece_data['data'] == 'target_data':
            selected_piece = session['selected_piece']
            selected_piece_position = session['selected_piece_position']
            target_piece = piece_data['target_piece']
            target_position = piece_data['target_box_position']
            selected_piece_legal_moves = moves.legal_moves(piece_position_table, selected_piece, selected_piece_position ,turn_total, session['can_castle_l'] , target_position  )

            if target_position not in selected_piece_legal_moves:
                status_code = 221 # error illegal move
                response_data = {'msg-type': 'error', 'msg':'illegal move made'}
            #elif selected_piece_legal_moves == 'checkMate':
             #   status_code = 231   
              #  response_data = {'msg-type': 'success', 'msg':'CheckMate'}
            else:
                print(selected_piece , target_position)
                if selected_piece == 'kl':
                    if target_position == 'G1':
                        print('run')
                        moves.update_board(piece_position_table, selected_piece, selected_piece_position, target_position)
                        moves.update_board(piece_position_table , 'rl' , 'H1' , 'F1')
                        response_data = {'msg_type': 'success', 'msg': 'legal move made', 'move_type': 'c'}
                        #c-> castle

                else:
                    moves.update_board(piece_position_table, selected_piece, selected_piece_position, target_position)
                    response_data = {'msg_type': 'success', 'msg': 'legal move made', 'move_type': 'normal'}
                turn_total += 1

                status_code = 211 # legal move

                if (selected_piece_position == 'H1' and session['can_castle_l'] == [0 , 1]) or (selected_piece_position == 'A1' and session['can_castle_l'] == [1,0]):
                    session['can_castle_l'] = [0 , 0]
                    print('afa  ')
                elif selected_piece_position == 'H1':
                    session['can_castle_l'] = [1 , 0]
                elif selected_piece_position == 'A1':
                     session['can_castle_l'] = [0 , 1]
                elif selected_piece_position == 'E1':
                     print('run 1')
                     session['can_castle_l'] = [0 , 0]

            session['piece_position_table'] = piece_position_table
            session['selected_piece'] = None
            session['selected_piece_position'] = None

            return jsonify(response_data), status_code
        
    return app