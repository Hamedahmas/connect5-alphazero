from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
from model import AlphaZeroNet
from mcts import MCTS, Node
from board import Board

app = Flask(__name__)
CORS(app)

model = AlphaZeroNet(rows=7, cols=9)
model.load_state_dict(torch.load("alphazero_model.pth", map_location=torch.device("cpu")))
model.eval()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def get_ai_move():
    data = request.get_json()
    state = data.get("state")

    board = Board(state=state)
    root = Node(board)
    mcts = MCTS(model)
    mcts.search(root)

    best_move = max(root.children.items(), key=lambda item: item[1].visits)[0]
    return jsonify({"move": best_move})

if __name__ == "__main__":
    app.run(debug=True)
