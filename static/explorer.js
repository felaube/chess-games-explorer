var movesHistory = [];

function move(board, chessKernel, selectedMove, moves)
{
    chessKernel.move(selectedMove);
    board.position(chessKernel.fen());
    movesHistory.push(selectedMove)
    
    var currentDict = moves;
    for (var i=0; i<movesHistory.length; i++)
    {
        currentDict = currentDict[movesHistory[i]]["next_moves"]
    }

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
        //spanMoveItem.setAttribute("onclick", "move(board, chessKernel, '" + currentMove + "', "+ movesDict + ")");
        let text = document.createTextNode(currentMove);
        spanMoveItem.appendChild(text)
        //spanMoveItem.setAttribute("onclick", "move(board, chessKernel, '" + text.textContent + "', "+ movesDict + ")");
        spanMoveItem.setAttribute("onclick", "move(board, chessKernel, '" + text.textContent + "', " + "moves)");
        //console.log(typeof(movesDict))
        //spanMoveItem.addEventListener("click", function(){move(board, chessKernel, "'" + this.textContent + "'", moves)});

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

        //spanMoveItem.onclick = move(board, chessKernel, currentMove);
        
    }

    //return movesList;
}