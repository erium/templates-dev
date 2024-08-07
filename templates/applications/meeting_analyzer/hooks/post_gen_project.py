import halerium_utilities as hu
import uuid

# assign new card ids
hu.file.assign_new_card_ids_to_tree('./')

target_id = "{{cookiecutter.chatBotCardID}}"
try:
    target_id = str(uuid.UUID(target_id, version=4))
except:
    target_id = str(uuid.uuid4())

board_path = "chatbot.board"
# set chatbot card id to target id
board = hu.board.Board.from_json(board_path)
for card in board.cards:
    if card.type == "bot":
        old_id = card.id
        card.id = target_id
        break  # only 1 card
# adapt connections
for edge in board.connections:
    if edge.connections.source.id == old_id:
        edge.connections.source.id = target_id
    if edge.connections.target.id == old_id:
        edge.connections.target.id = target_id
board.to_json(board_path)

print("Hal_Magic_Template_done.")
