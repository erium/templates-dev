import os
import shutil
import halerium_utilities as hu
from halerium_utilities import notebook

# Select the specified template
model_templates = '{{cookiecutter.use_case_slug}}'
hu.file.card_ids.assign_new_card_ids_to_tree('./')

# Adding cards, connections, and links on experiments board in project template
project_path = './../hypotheses_experiments_learnings.board'


if os.path.exists(project_path):
    board = hu.file.io.read_board(project_path)
    board_titles = [x['title'] for x in board['nodes']]
    experiment_count = board_titles.count('Experiment')
    y_pos = 178 + (155 * experiment_count)
    
    learning_card = hu.board.board.create_card(title='Learning',
                                               content='Enter learning here',
                                               position={
                                                   "x": 935.066650390625, "y": y_pos},
                                               size={"width": 100,
                                                     "height": 130},
                                               color="#125059")
    learning_card_id = learning_card['id']

    experiment_card = hu.board.board.create_card(title='Experiment',
                                                 content='Data Preparation',
                                                 position={
                                                     "x": 690.816650390625, "y": y_pos},
                                                 size={"width": 100,
                                                       "height": 130},
                                                 color="#28337e")
    experiment_card_id = experiment_card['id']

    hypo_ques_card = hu.board.board.create_card(title='Hypothesis/Question',
                                                content='*Enter hypothesis here*',
                                                position={
                                                    "x": 371.254150390625, "y": y_pos},
                                                size={"width": 173,
                                                      "height": 130},
                                                color="#513063")
    hypo_ques_card_id = hypo_ques_card['id']

    # Add cards to board
    hu.board.board.add_card_to_board(project_path, learning_card)
    hu.board.board.add_card_to_board(project_path, experiment_card)
    hu.board.board.add_card_to_board(project_path, hypo_ques_card)

    # Add connections between cards
    hu.board.board.create_card_connection(
        project_path, hypo_ques_card_id, experiment_card_id, 'right', 'left')
    hu.board.board.create_card_connection(
        project_path, experiment_card_id, learning_card_id, 'right', 'left')

    # Add link to notebook
    notebook_dict = {'data_preparation': 'data_preparation.ipynb'}
    notebook_path = notebook_dict[model_templates]
    notebook.link.create_card_cell_link(
        experiment_card_id, notebook_path, 1)
