import os

from flask import ( 
    Flask, render_template, request, session, url_for
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

    # a simple page that says hello
    @app.route('/')
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
        
        piece_position = {
            "A1":"rl", "B1":"nl", "C1":"bl", "D1":"ql", "E1":"kl", "F1":"nl", "G1":"bl", "H1":"rl", 
            "A8":"rd", "B8":"nd", "C8":"bd", "D8":"qd", "E8":"kd", "F8":"nd", "G8":"bd", "H8":"rd" 
            }
        

        # Adding pawns
        for i in range(8):
            piece_position[chr(65+i) + '2'] = "pl"
            piece_position[chr(65+i) + '7'] = "pd"


        return render_template('index.html', piece_position=piece_position)

    return app