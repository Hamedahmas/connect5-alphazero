const ROWS = 7;
const COLS = 9;
let board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
let currentPlayer = 1;
let gameOver = false;

function renderBoard() {
    const boardDiv = document.getElementById("board");
    boardDiv.innerHTML = "";
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            if (board[r][c] === 1) cell.classList.add("player1");
            else if (board[r][c] === -1) cell.classList.add("player2");
            cell.addEventListener("click", () => handleClick(c));
            boardDiv.appendChild(cell);
        }
    }
}

function handleClick(col) {
    if (gameOver || currentPlayer !== 1) return;

    for (let r = ROWS - 1; r >= 0; r--) {
        if (board[r][col] === 0) {
            board[r][col] = 1;
            currentPlayer = -1;
            renderBoard();
            checkWinner();
            aiMove();
            return;
        }
    }
}

function aiMove() {
    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: board })
    })
    .then(res => res.json())
    .then(data => {
        const col = data.move;
        for (let r = ROWS - 1; r >= 0; r--) {
            if (board[r][col] === 0) {
                board[r][col] = -1;
                currentPlayer = 1;
                renderBoard();
                checkWinner();
                return;
            }
        }
    });
}

function checkWinner() {
    // optional: می‌تونی الگوریتم بررسی بردن را اضافه کنی
}

renderBoard();
