import main.moves as moves

_, pos = moves.read_FEN('rnbqk2r/ppp3pp/2nb1p2/8/2BP4/2N2N2/PPP2PPP/R1BQR1K1 b kq - 0 1')
print(moves.is_checkmate(pos, 1, {'l':'', 'd':'KQ'}))