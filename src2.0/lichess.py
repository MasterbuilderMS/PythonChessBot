import berserk
import random

TOKEN = "lip_KY7PMgDuITXRvhrffx7a"
session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)


def accept_challenges_and_play():
    print("Waiting for challenges...")
    for event in client.bots.stream_incoming_events():
        print(f"Incoming event: {event}")

        if event["type"] == "challenge":
            challenge = event["challenge"]
            challenge_id = challenge["id"]
            print(
                f"Received challenge from {challenge['challenger']['id']} - Variant: {challenge['variant']['key']}, Rated: {challenge['rated']}"
            )
            try:
                client.bots.accept_challenge(challenge_id)
                print(f"Accepted challenge {challenge_id}")
            except berserk.exceptions.ResponseError as e:
                print(
                    f"Error accepting challenge {challenge_id}: {e}, Details: {e.args}"
                )

        elif event["type"] == "gameStart":
            game_id = event["game"]["id"]
            print(f"Game started: {game_id}")
            play_game(game_id)


def play_game(game_id):
    print(f"Playing game {game_id}")
    for event in client.bots.stream_game_state(game_id):
        # Print event for debugging
        print(f"Game event: {event}")

        if event["type"] == "gameFull":
            # Game started, you can initialize any game state here if needed
            print("GameFull received.")

        elif event["type"] == "chatLine":
            # Ignore chat events for now
            continue

        elif event["type"] == "gameState":
            # Check if it's our turn
            if event["status"] != "started":
                print(f"Game ended with status {event['status']}")
                break

            is_my_turn = event["isMyTurn"]
            if is_my_turn:
                moves = event["moves"].split() if event["moves"] else []
                print(f"Moves played so far: {moves}")

                # Get all legal moves for this position
                legal_moves = client.bots.get_legal_moves(game_id)

                if not legal_moves:
                    print("No legal moves available, game might be over.")
                    break

                # Pick a random legal move
                chosen_move = random.choice(legal_moves)
                print(f"Playing move: {chosen_move}")

                try:
                    client.bots.make_move(game_id, chosen_move)
                    print(f"Move {chosen_move} played successfully.")
                except berserk.exceptions.ResponseError as e:
                    print(f"Failed to make move {chosen_move}: {e}")


if __name__ == "__main__":
    accept_challenges_and_play()
