import os

from flask import ( 
    Flask, render_template, request, session, url_for, flash
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

        # piece_position, curr_turn, moves, players -> session variables
        return render_template('index.html', piece_position=piece_position)

    return app