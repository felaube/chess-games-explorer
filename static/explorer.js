function move(board, chessKernel, selectedMove, moves)
{
    chessKernel.move(selectedMove);
    board.position(chessKernel.fen());
    movesHistory.push(selectedMove);
    currentMoveIndex = movesHistory.length;
    
    var currentDict = moves;
    var movesHistoryElement = document.getElementById("movesHistory")
    var movesString = "";
    for (var i=0; i<movesHistory.length; i++)
    {
        currentDict = currentDict[movesHistory[i]]["next_moves"]
        if (i % 2 == 0)
        {
            movesString += (i / 2 + 1).toString() + ". ";
        }
        movesString += movesHistory[i] + " ";
    }

    movesHistoryElement.innerHTML = movesString;
    

    createMovesList(currentDict)
}

function createMovesList(movesDict)
{
    var movesList = document.getElementById("movesList")

    while(movesList.firstChild)
    {
        movesList.removeChild(movesList.firstChild);
    }

    for (currentMove in movesDict)
    {
        let white_percentage = movesDict[currentMove]["white_percentage"].toString();
        let draw_percentage = movesDict[currentMove]["draw_percentage"].toString();
        let black_percentage = movesDict[currentMove]["black_percentage"].toString();

        let movesListItem = document.createElement("li");
        movesListItem.classList.add("moves-list-element");

        let progressItem = document.createElement("div");
        progressItem.classList.add("progress");

        let moveItem = document.createElement("div");
        moveItem.classList.add("move");

        let spanMoveItem = document.createElement("span");
        spanMoveItem.classList.add("cursor-pointer");
        let text = document.createTextNode(currentMove);
        spanMoveItem.appendChild(text)
        spanMoveItem.setAttribute("onclick", "move(board, chessKernel, '" + text.textContent + "', " + "moves)");

        moveItem.appendChild(spanMoveItem);

        let moveCountItem = document.createElement("div");
        let spanMoveCountItem = document.createElement("span");
        spanMoveCountItem.classList.add("move-count");
        text = document.createTextNode(movesDict[currentMove]["count"]);
        spanMoveCountItem.appendChild(text)

        moveCountItem.appendChild(spanMoveCountItem);

        let percentageBarWhite = document.createElement("div");
        percentageBarWhite.classList.add("progress-bar", "percentage-bar", "bar-white");
        percentageBarWhite.setAttribute("role", "progressbar");
        percentageBarWhite.style.width = white_percentage + "%"; 
        percentageBarWhite.setAttribute("aria-valuenow", white_percentage);
        percentageBarWhite.setAttribute("aria-valuemin", "0");
        percentageBarWhite.setAttribute("aria-valuemax", white_percentage);
        text = document.createTextNode(white_percentage + "%");
        percentageBarWhite.appendChild(text)

        let percentageBarDraw = document.createElement("div");
        percentageBarDraw.classList.add("progress-bar", "percentage-bar", "bar-draw");
        percentageBarDraw.setAttribute("role", "progressbar");
        percentageBarDraw.style.width = draw_percentage + "%"; 
        percentageBarDraw.setAttribute("aria-valuenow", draw_percentage);
        percentageBarDraw.setAttribute("aria-valuemin", "0");
        percentageBarDraw.setAttribute("aria-valuemax", draw_percentage);
        text = document.createTextNode(draw_percentage + "%");
        percentageBarDraw.appendChild(text)

        let percentageBarBlack = document.createElement("div");
        percentageBarBlack.classList.add("progress-bar", "percentage-bar", "bar-black");
        percentageBarBlack.setAttribute("role", "progressbar");
        percentageBarBlack.style.width = black_percentage + "%"; 
        percentageBarBlack.setAttribute("aria-valuenow", black_percentage);
        percentageBarBlack.setAttribute("aria-valuemin", "0");
        percentageBarBlack.setAttribute("aria-valuemax", black_percentage);
        text = document.createTextNode(black_percentage + "%");
        percentageBarBlack.appendChild(text)
        
        progressItem.appendChild(moveItem);
        progressItem.appendChild(moveCountItem);
        progressItem.appendChild(percentageBarWhite);
        progressItem.appendChild(percentageBarDraw);
        progressItem.appendChild(percentageBarBlack);
        
        movesListItem.appendChild(progressItem);
        
        movesList.appendChild(movesListItem);
        
    }

}

function reset(board, chessKernel)
{
    board.start();
    chessKernel.reset();
    movesHistory = [];
    var movesHistoryElement = document.getElementById("movesHistory");
    movesHistoryElement.innerHTML = "";
    createMovesList(moves);
}

function goBack(board, chessKernel, moves)
{   
    if (currentMoveIndex == 0)
    {
        return
    }

    var currentDict = moves;
    chessKernel.reset();

    currentMoveIndex -= 1;

    for (var i=0; i<currentMoveIndex; i++)
    {
        chessKernel.move(movesHistory[i]);
        currentDict = currentDict[movesHistory[i]]["next_moves"]
    }

    board.position(chessKernel.fen());
    createMovesList(currentDict);
}

function goForward(board, chessKernel, moves)
{
    if (currentMoveIndex >= movesHistory.length)
    {
        return
    }
    var currentDict = moves;
    currentMoveIndex += 1;

    for (let i=0; i<currentMoveIndex; i++)
    {        
        currentDict = currentDict[movesHistory[i]]["next_moves"];
    }

    chessKernel.move(movesHistory[currentMoveIndex - 1]);    

    board.position(chessKernel.fen());
    createMovesList(currentDict);
}

function changeCaret()
{
    //if (document.getElementById("filterCaret").classList.contains("fa-caret-right"))
    //{
    //    document.getElementById("filterCaret").toggleClass("fa-caret-right fa-caret-down");
    //}

    //else if (document.getElementById("filterCaret").classList.contains("fa-caret-down"))
    //{
    //  document.getElementById("filterCaret").toggleClass("fa-caret-down fa-caret-right");
    //}
    this.find('i').toggleClass("fa-caret-right fa-caret-down");
}
