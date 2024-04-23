from . import moves
from . import pieces
import os
import json
import random

from flask import ( 
    Flask, render_template, request, session, url_for, flash, jsonify , sessions, redirect    
)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SESSION_COOKIE_SAMESITE='strict',
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
        if 'app_url' not in session:
            session['app_url'] = APP_URL

        if 'game_start' not in session:
            session['game_start'] = False

        if 'players' not in session:
            session['players'] = {'p1':{}, 'p2':{}}

        if request.method == "POST" and 'play' in request.form:
            session['game_start'] = True
            return redirect('/game')

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('index.html')        

    @app.route('/game', methods=('GET', 'POST'))
    def game():
        if 'game_start' not in session or not session['game_start']:
            return redirect('/')
        
        if not session['players'] or 'username' not in session['players']['p1'] or 'username' not in session['players']['p2']:
            return redirect('/')
        
        if 'piece_position_table' not in session:
            _, session['piece_position_table'] = moves.read_FEN(START_POSITION)

        if 'can_castle' not in session:
            session['can_castle'] = {'l':'kq', 'd':'kq'}
            # keys -> the players
            # k -> king side castling, q -> queen side castling

        if 'turn_total' not in session:
            session['turn_total'] = 0

        if 'app_url' not in session:
            session['app_url'] = APP_URL

        if 'piece_colour' not in session['players']['p1'] or 'piece_colour' not in session['players']['p2']:
            players = session['players']
            # Randomly assign piece colours to player
            players['p1']['piece_colour'] = random.choice('ld')
            players['p2']['piece_colour'] = 'ld'[players['p1']['piece_colour'] == 'l']

            session['players'] = players

        if session['players']['p1']['piece_colour'] == 'l':
            player_username_l = session['players']['p1']['username']
            player_username_d = session['players']['p2']['username']
        else:
            player_username_l = session['players']['p2']['username']
            player_username_d = session['players']['p1']['username']

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('game.html', player_username_l=player_username_l, player_username_d=player_username_d)

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
        
        if request.method == "POST" and 'reset' in request.form:
            session.clear()

        elif request.method == "POST" and 'set' in request.form:
            custom_position = request.form['fen_position']

            # Implement valid FEN string check
            try:
                player_to_move, session['piece_position_table'] = moves.read_FEN(custom_position)
                session['turn_total'] = [0, 1][player_to_move == 'b']

            except:
                flash('Invalid FEN string')

        if 'piece_position_table' not in session:
            _, session['piece_position_table'] = moves.read_FEN(START_POSITION)

        if 'app_url' not in session:
            session['app_url'] = APP_URL

        if 'can_castle' not in session:
            session['can_castle'] = {'l':'kq', 'd':'kq'}

        if 'turn_total' not in session:
            session['turn_total'] = 0

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('dev.html')
    
    @app.route('/login', methods=['POST'])
    def login():
        if 'players' not in session:
            return 'Unauthorized Access', 401

        if request.method == "POST" and 'player_login_p1' in request.form:
            players = session['players']

            username = request.form['username']
            players['p1']['username'] = username
            session['players'] = players

        if request.method == "POST" and 'player_login_p2' in request.form:
            players = session['players']

            username = request.form['username']
            players['p2']['username'] = username
            session['players'] = players

        '''
        To add:
        Input Validation: Contains alphabets, a specific length, doesn't contain profanity.
        DB integration: Check if user exists, Password verification.
        '''

        return redirect('/')
    
    @app.route('/logout', methods=['POST'])
    def logout():
        if 'players' not in session:
            return 'Unauthorized Access', 401

        if request.method == "POST" and 'logout_p1' in request.form:
            players = session['players']
            players['p1'] = {}
            session['players'] = players

        if request.method == "POST" and 'logout_p2' in request.form:
            players = session['players']
            players['p2'] = {}
            session['players'] = players

        return redirect('/')

    @app.route('/process_move', methods=['POST'])
    def process_move():
        '''
        Custom HTTP Status Codes
        210 -> Successfully received selected_piece info
        211 -> Legal piece move made
        221 -> Illegal piece move made
        231 -> CheckMate
        '''
        piece_data = request.json

        if 'selected_piece' not in session:
            session['selected_piece'] = None
        
        if 'selected_piece_position' not in session:
            session['selected_piece_position'] = None

        piece_position_table = session['piece_position_table']

        if piece_data['data'] == 'initial_data':
            session['selected_piece'] = piece_data['selected_piece']
            session['selected_piece_position'] = piece_data['selected_piece_position']         
            legal_moves = moves.legal_moves(session['piece_position_table'], session['selected_piece'], session['selected_piece_position'], session['turn_total'], session['can_castle'])
            response_data = {'legal_moves': legal_moves}
            
            status_code = 210

            return jsonify(response_data), status_code
        
        if piece_data['data'] == 'target_data':
            selected_piece = session['selected_piece']
            selected_piece_position = session['selected_piece_position']
            can_castle = session['can_castle']
            turn_total = session['turn_total']

            target_piece = piece_data['target_piece']
            target_position = piece_data['target_box_position']
                
            selected_piece_legal_moves = moves.legal_moves(piece_position_table, selected_piece, selected_piece_position, turn_total, can_castle)

            if target_position not in selected_piece_legal_moves:
                status_code = 221 # error illegal move
                response_data = {'msg-type': 'error', 'msg':'illegal move made'}
            else:
                selected_piece_type, selected_piece_colour = selected_piece

                if selected_piece_type == 'k' and selected_piece_position[0] == "E" and target_position[0] in 'CG': # target_position column
                    # Handle castling
                    
                    # selected_piece_postion = E1/E8
                    # target_position = G1/G8/C1/C8
                    # If E<G -> king side castle
                    # If E>C -> queen side castle

                    rook_init_position = 'AH'[selected_piece_position[0] < target_position[0]] + selected_piece_position[1]
                    rook_target_position = 'DF'[rook_init_position[0] == 'H'] + selected_piece_position[1]

                    moves.update_board(piece_position_table, selected_piece, selected_piece_position, target_position)
                    moves.update_board(piece_position_table, 'r' + selected_piece_colour, rook_init_position, rook_target_position) 

                    if target_position[0] == 'G':
                        can_castle[selected_piece_colour] = can_castle[selected_piece_colour].replace('k', '')
                    else:
                        can_castle[selected_piece_colour] = can_castle[selected_piece_colour].replace('q', '')

                    response_data = {'msg_type': 'success', 'msg': 'legal move made', 'move_type': 'c'} #c-> castle
                else:
                    # Remove castling ability when king/rook moved (not castle)
                    if can_castle[selected_piece_colour] and selected_piece_type == 'k': # Piece being moves is a king (not castle)
                        can_castle[selected_piece_colour] = ''
                    elif can_castle[selected_piece_colour] and selected_piece_type == 'r' and selected_piece_position > 'E':
                        can_castle[selected_piece_colour] = can_castle[selected_piece_colour].replace('k', '')
                    elif can_castle[selected_piece_colour] and selected_piece_type == 'r':
                        can_castle[selected_piece_colour] = can_castle[selected_piece_colour].replace('q', '')

                    moves.update_board(piece_position_table, selected_piece, selected_piece_position, target_position)

                    move_flag = [['capture', 'move'][target_piece == ''], 'check'][moves.in_check(piece_position_table, turn_total+1, can_castle)]
                    response_data = {'msg_type': 'success', 'msg': 'legal move made', 'move_type': 'normal', 'move_flag':move_flag}
                
                turn_total += 1 # legal move made by current player

                # check game state immediately after it is opponent's turn
                if moves.is_checkmate(piece_position_table, turn_total, can_castle):
                    game_result = ['1-0','0-1'][turn_total % 2 == 0]

                    response_data['game_state'] = 'checkmate' 
                    response_data['game_result'] = game_result
                    status_code = 231

                    return jsonify(response_data), status_code

                status_code = 211 # legal move
                
            session['piece_position_table'] = piece_position_table
            session['turn_total'] = turn_total
            session['can_castle'] = can_castle
            session['selected_piece'] = None
            session['selected_piece_position'] = None

            return jsonify(response_data), status_code
        
    return app