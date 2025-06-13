import berserk
import chess
import random

TOKEN = "lip_KY7PMgDuITXRvhrffx7a"
session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)


def play_game(game_id):
    board = chess.Board()
    print(f"Playing game {game_id}")

    for event in client.bots.stream_game_state(game_id):
        if event["type"] == "gameFull":
            print("Game started")
        elif event["type"] == "gameState":
            moves = event["moves"].split()
            board.reset()
            for move in moves:
                board.push_uci(move)

            if event.get("isYourTurn", False):
                legal_moves = list(board.legal_moves)
                if not legal_moves:
                    print("No legal moves, game likely over")
                    break

                move = random.choice(legal_moves)
                print(f"Playing move: {move.uci()}")
                try:
                    client.bots.make_move(game_id, move.uci())
                except berserk.exceptions.ResponseError as e:
                    print(f"Failed to make move: {e}")

            if event.get("status") in ["mate", "resign", "draw", "outoftime"]:
                print(f"Game ended with status: {event['status']}")
                break


def accept_challenges():
    print("Waiting for challenges...")
    for event in client.bots.stream_incoming_events():
        print(f"Incoming event: {event}")

        if event["type"] == "challenge":
            challenge_id = event["challenge"]["id"]
            print(f"Accepting challenge {challenge_id}")
            try:
                client.bots.accept_challenge(challenge_id)
            except berserk.exceptions.ResponseError as e:
                print(f"Error accepting challenge: {e}")

        elif event["type"] == "gameStart":
            game_id = event["game"]["id"]
            play_game(game_id)


if __name__ == "__main__":
    accept_challenges()
