function move(board, chessKernel, selectedMove)
{
    chessKernel.move(selectedMove);
    board.position(chessKernel.fen());
}