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

    from . import moves

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
        
        start_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' # FEN str for starting position
        global piece_position

        piece_position = moves.read_FEN(start_position) # FEN -> Game Notation
        if request.method == "POST" and 'reset' in request.form:
            piece_position = moves.read_FEN(start_position)

        elif request.method == "POST" and 'set' in request.form:
            custom_position = request.form['fen_position']

            # Implement valid FEN string check
            try:
                piece_position = moves.read_FEN(custom_position)
            except:
                flash('Invalid FEN string')
        elif request.method == "POST":
            print(request.json)

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('index.html', piece_position=piece_position, app_url=APP_URL)

    @app.route('/process_move', methods=['POST'])
    def process_move():
        piece_data = request.json

        if piece_data['data'] == 'initial_data':
            session['selected_piece'] = piece_data['selected_piece']
            session['selected_piece_position']= piece_data['selected_piece_position']         
            legal_moves = moves.legal_moves(piece_position, session['selected_piece'], session['selected_piece_position'])
            response_data = {'legal_moves': legal_moves}
            return jsonify(response_data), 200
        if piece_data['data'] == 'target_data':
            target_box = piece_data['target_box']
            target_row = piece_data['target_row']
            target_position = target_box+target_row
            piece_position[target_position] = session['selected_piece']
            del piece_position[session['selected_piece_position']]
            
        


        return '1'

    return app