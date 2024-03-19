from . import moves
import os
import json

from flask import ( 
    Flask, render_template, request, session, url_for, flash, jsonify , sessions    
)

def create_app(test_config=None):
    # create and configure the app
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

        if 'piece_position_table' not in session:
            session['piece_position_table'] = moves.read_FEN(START_POSITION)

        if 'app_url' not in session:
            session['app_url'] = APP_URL

        if request.method == "POST" and 'reset' in request.form:
            session['piece_position_table'] = moves.read_FEN(START_POSITION)

        elif request.method == "POST" and 'set' in request.form:
            custom_position = request.form['fen_position']

            # Implement valid FEN string check
            try:
                session['piece_position_table'] = moves.read_FEN(custom_position)
            except:
                flash('Invalid FEN string')

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('index.html')

    @app.route('/process_move', methods=['POST'])
    def process_move():
        '''
        Custom HTTP Status Codes
        240 -> Successfully received selected_piece info
        241 -> Legal piece move made
        441 -> Illegal piece move made
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

            legal_moves = moves.legal_moves(session['piece_position_table'], session['selected_piece'], session['selected_piece_position'])
            response_data = {'legal_moves': legal_moves}
            
            status_code = 210

            return jsonify(response_data), status_code
        
        if piece_data['data'] == 'target_data':
            selected_piece = session['selected_piece']
            selected_piece_position = session['selected_piece_position']
            target_piece = piece_data['target_piece']
            target_position = piece_data['target_box_position']

            selected_piece_legal_moves = moves.legal_moves(piece_position_table, selected_piece, selected_piece_position)

            if target_position not in selected_piece_legal_moves:
                status_code = 221 # error illegal move
                response_data = {'msg-type': 'error', 'msg':'illegal move made'}
            else:
                status_code = 211 # legal capture
                piece_position_table[target_position] = selected_piece
                del piece_position_table[selected_piece_position]
                response_data = {'msg-type': 'success', 'msg': 'legal move made'}

            session['piece_position_table'] = piece_position_table
            session['selected_piece'] = None
            session['selected_piece_position'] = None

            return jsonify(response_data), status_code
        
    return app