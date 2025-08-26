import chess.pgn
import chess.polyglot

def filter_pgn(input_pgn: str, output_pgn: str):
    with open(input_pgn, "r", encoding="utf-8") as infile, \
         open(output_pgn, "w", encoding="utf-8") as outfile:
        
        while True:
            game = chess.pgn.read_game(infile)
            if game is None:
                break  # no more games
            
            # 1. Keep only draws
            if game.headers.get("Result") != "1/2-1/2":
                continue
            
            # 2. White must be Nimsilubot
            if game.headers.get("White") != "Nimsilubot":
                continue
            
            # 3. First moves must be 1. Nf3 d5
            board = game.board()
            moves = list(game.mainline_moves())
            if len(moves) < 2:
                continue
            if not (board.san(moves[0]) == "Nf3" and 
                    board.san(moves[1]) == "d5"):
                continue
            
            # Passed all filters, write game
            print(game, file=outfile, end="\n\n")


def convert_pgn_to_bin(pgn_file: str, bin_file: str):
    with open(pgn_file, "r", encoding="utf-8") as reader, \
         chess.polyglot.Writer(open(bin_file, "wb")) as writer:
        
        while True:
            game = chess.pgn.read_game(reader)
            if game is None:
                break
            
            board = game.board()
            for move in game.mainline_moves():
                entry = chess.polyglot.Entry.from_board(board, move, weight=1, learn=0)
                writer.write(entry)
                board.push(move)


if __name__ == "__main__":
    input_pgn = "axn.pgn"
    output_pgn = "axon.pgn"
    output_bin = "axon.bin"
    
    filter_pgn(input_pgn, output_pgn)
    convert_pgn_to_bin(output_pgn, output_bin)
    print("✅ Generated axon.pgn and axon.bin")
