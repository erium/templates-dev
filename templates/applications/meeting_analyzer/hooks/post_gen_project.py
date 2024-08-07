import halerium_utilities as hu
import uuid

from halerium_utilities.board import Board

# assign new card ids
hu.file.assign_new_card_ids_to_tree('./')

target_id = "{{cookiecutter.chatbot_card_id}}"
try:
    target_id = str(uuid.UUID(target_id, version=4))
except:
    target_id = str(uuid.uuid4())

# set chatbot card id to target id
board = Board.from_json("chatbot.board")
for card in board.cards:
    if card.type == "bot":
        card.id = target_id
        break  # only 1 card
board.to_json("chatbot.board")

print("Hal_Magic_Template_done.")
