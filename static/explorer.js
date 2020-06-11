/**
 * Handles the move, when it selected from the database.
 * @param {object} board Described in static/board
 * @param {object} chessKernel Described in static/chess
 * @param {string} selectedMove 
 * @param {object} moves JSON parsed from Python dict, constructed in app.py
 */
function moveFromDatabase(board, chessKernel, selectedMove, moves)
{
    // Send move to kernel and update the board 
    chessKernel.move(selectedMove);
    board.position(chessKernel.fen());

    // Add move to history array
    updateHistory(selectedMove)

    var currentDict = moves;
    for (let i=0; i<currentMoveIndex; i++)
    {
        // Find the "next_moves" in the database from the current position
        currentDict = currentDict[movesHistory[i]]["next_moves"]
    }

    createMovesList(currentDict)
    createMovesLinks();
}

/**
 * Recreates the HTML elements corresponding to the database at a specific position, given by movesDict 
 * @param {object} movesDict 
 */
function createMovesList(movesDict)
{
    var movesList = document.getElementById("movesList")

    // Remove all elements of the "movesList" element
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
        spanMoveItem.setAttribute("onclick", "moveFromDatabase(board, chessKernel, '" + text.textContent + "', " + "moves)");

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
        
        let percentageBarWhiteSpan = document.createElement("span");
        text = document.createTextNode(white_percentage + "%");
        percentageBarWhiteSpan.setAttribute("title", text.textContent);
        percentageBarWhiteSpan.appendChild(text);

        if (parseInt(white_percentage) < 20)
        {
            percentageBarWhiteSpan.classList.add("white-percentage-hidden");
        }

        percentageBarWhite.appendChild(percentageBarWhiteSpan)

        let percentageBarDraw = document.createElement("div");
        percentageBarDraw.classList.add("progress-bar", "percentage-bar", "bar-draw");
        percentageBarDraw.setAttribute("role", "progressbar");
        percentageBarDraw.style.width = draw_percentage + "%"; 
        percentageBarDraw.setAttribute("aria-valuenow", draw_percentage);
        percentageBarDraw.setAttribute("aria-valuemin", "0");
        percentageBarDraw.setAttribute("aria-valuemax", draw_percentage);

        let percentageBarDrawSpan = document.createElement("span");
        text = document.createTextNode(draw_percentage + "%");
        percentageBarDrawSpan.setAttribute("title", text.textContent);
        percentageBarDrawSpan.appendChild(text);

        if (parseInt(draw_percentage) < 20)
        {
            percentageBarDrawSpan.classList.add("draw-percentage-hidden");
        }

        percentageBarDraw.appendChild(percentageBarDrawSpan)

        let percentageBarBlack = document.createElement("div");
        percentageBarBlack.classList.add("progress-bar", "percentage-bar", "bar-black");
        percentageBarBlack.setAttribute("role", "progressbar");
        percentageBarBlack.style.width = black_percentage + "%"; 
        percentageBarBlack.setAttribute("aria-valuenow", black_percentage);
        percentageBarBlack.setAttribute("aria-valuemin", "0");
        percentageBarBlack.setAttribute("aria-valuemax", black_percentage);

        let percentageBarBlackSpan = document.createElement("span");
        text = document.createTextNode(black_percentage + "%");
        percentageBarBlackSpan.setAttribute("title", text.textContent);
        percentageBarBlackSpan.appendChild(text);

        if (parseInt(black_percentage) < 20)
        {
            percentageBarBlackSpan.classList.add("black-percentage-hidden");
        }

        percentageBarBlack.appendChild(percentageBarBlackSpan)
        
        progressItem.appendChild(moveItem);
        progressItem.appendChild(moveCountItem);
        progressItem.appendChild(percentageBarWhite);
        progressItem.appendChild(percentageBarDraw);
        progressItem.appendChild(percentageBarBlack);
        
        movesListItem.appendChild(progressItem);
        
        movesList.appendChild(movesListItem);
    }
}

/**
 * Reset everything as if the user refreshed the page 
 * @param {object} board 
 * @param {object} chessKernel 
 */
function reset(board, chessKernel)
{
    board.start();
    chessKernel.reset();
    movesHistory = [];
    currentMoveIndex = 0;
    positionInDatabase = true

    createMovesList(moves);
    clearMovesLinks();
}

/**
 * Go back 1 or more moves in the history, displaying previous positions on the board
 * @param {object} board 
 * @param {object} chessKernel 
 * @param {object} moves 
 * @param {number} nTimes 
 */
function goBack(board, chessKernel, moves, nTimes=1)
{   
    // Check if the resulting position would be prior to the starting position
    if (currentMoveIndex - nTimes < 0)
    {
        return
    }

    unsetHighlightedMove();

    var currentDict = moves;
    chessKernel.reset();
    positionInDatabase = true;

    currentMoveIndex -= nTimes;

    // Move on the kernel once at a time, and check if the position can be found in the databse
    for (let i=0; i<currentMoveIndex; i++)
    {
        chessKernel.move(movesHistory[i]);
        try
        {
            currentDict = currentDict[movesHistory[i]]["next_moves"]
        }
        catch(err)
        {
            // If an error was caught, it means the position is not in the database
            positionInDatabase = false;
        }
    }

    board.position(chessKernel.fen());
    
    if (positionInDatabase)
    {
        createMovesList(currentDict);
    }

    // If currentMoveIndex is 0, we are at the starting position, so, there is no move to be highlighted
    if (currentMoveIndex != 0)
    {
        setHighlightedMove();
    }
}

/**
 * Go forward 1 or more moves in the history, restoring positions set by goBack
 * @param {object} board 
 * @param {object} chessKernel 
 * @param {object} moves 
 * @param {number} nTimes 
 */
function goForward(board, chessKernel, moves, nTimes=1)
{
    // Check if the resulting index would go beyond the game set currently in movesHistory
    if (currentMoveIndex + nTimes > movesHistory.length)
    {
        return
    }

    // If currentMoveIndex is 0, we are at the starting position, so, there is no move highlighted
    if (currentMoveIndex != 0)
    {
        unsetHighlightedMove();
    }

    var currentDict = moves;
    chessKernel.reset();
    currentMoveIndex += nTimes;

    // Move on the kernel once at a time, and check if the position can be found in the databse
    for (let i=0; i<currentMoveIndex; i++)
    {
        chessKernel.move(movesHistory[i]);
        try
        {
            currentDict = currentDict[movesHistory[i]]["next_moves"];
        }
        catch(err)
        {
            // If an error was caught, it means the position is not in the database
            positionInDatabase = false;
        }
    }

    if (positionInDatabase)
    {
        createMovesList(currentDict);
    }
    else
    {
        movesList.innerHTML = "There are no games that reached this position";
    }
    
    board.position(chessKernel.fen());
    setHighlightedMove();
}

/**
 * Modifies the icon of the caret when clicked
 */
function changeCaret()
{
    this.find('i').toggleClass("fa-caret-right fa-caret-down");
}

// Function from https://chessboardjs.com/examples.html#5000
function onDragStart (source, piece, position, orientation) {
    // do not pick up pieces if the game is over
    if (chessKernel.game_over()) return false
  
    // only pick up pieces for the side to move
    if ((chessKernel.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (chessKernel.turn() === 'b' && piece.search(/^w/) !== -1)) {
      return false
    }
}

// Function modified from https://chessboardjs.com/examples.html#5000
function onDrop (source, target) {
    // see if the move is legal
    var move = chessKernel.move({
      from: source,
      to: target,
      promotion: 'q' // NOTE: always promote to a queen for example simplicity
    })
  
    // illegal move
    if (move === null) return 'snapback'
  
    onDropCreateMoveList(moves, move["san"])
}

// Function from https://chessboardjs.com/examples.html#5000
// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
    board.position(chessKernel.fen())
}

/**
 * Handles the move, when it is made dragging a piece on the board
 * @param {object} movesDict 
 * @param {string} selectedMove 
 */
function onDropCreateMoveList(movesDict, selectedMove)
{
    if (positionInDatabase)
    {
        currentDict = movesDict;
        // Iterate to get to the moves currently shown
        for (var i=0; i<currentMoveIndex; i++)
        {
            currentDict = currentDict[movesHistory[i]]["next_moves"];
        }
    }
    else
    {
        currentDict = [];
    }
    
    // Add another move
    updateHistory(selectedMove)

    // Check if this position is in the database
    if (selectedMove in currentDict)
    {
        createMovesList(currentDict[selectedMove]["next_moves"]);
    }
    else
    {
        positionInDatabase = false;
        var movesList = document.getElementById("movesList")

        while(movesList.firstChild)
        {
            movesList.removeChild(movesList.firstChild);
        }

        movesList.innerHTML = "There are no games that reached this position";
    }

    createMovesLinks()
}

/**
 * Updates movesHistory variable, when needed, adding a new move, or just incrementing the currentMoveIndex variable
 * @param {string} selectedMove 
 */
function updateHistory(selectedMove)
{
    // Updates the number of moves and add it to the history
    if (movesHistory[currentMoveIndex] == selectedMove)
    {
        // If the move is already in the history at the right place,
        // just increment currentMoveIndex
        currentMoveIndex += 1;
        return;
    }

    movesHistory[currentMoveIndex] = selectedMove; 
    currentMoveIndex += 1;
    
    // Remove every move that has become obsolete 
    movesHistory.splice(currentMoveIndex, movesHistory.length - currentMoveIndex);
}

/**
 * Creates the clickable items shown above the moves database
 */
function createMovesLinks()
{
    var movesLink = document.getElementById("movesHistory")

    clearMovesLinks()

    for (let i = 0; i < movesHistory.length; i++)
    {
        currentMove = movesHistory[i]
        
        let moveItem = document.createElement("div");
        moveItem.classList.add("move-history");

        let spanMoveItem = document.createElement("span");
        spanMoveItem.classList.add("cursor-pointer");

        if (i % 2 == 0)
        {
            // Move made by white
            var text = document.createTextNode((i / 2 + 1).toString() + ". " + currentMove);
        }
        else
        {
            // Move made by black
            var text = document.createTextNode(" " + currentMove);    
        }
        spanMoveItem.appendChild(text)
        spanMoveItem.setAttribute("onclick", "goToPosition(" + i + ")");
        
        moveItem.appendChild(spanMoveItem)
        movesLink.appendChild(moveItem)
    }

    movesLink.children[currentMoveIndex - 1].classList.add("current-move");
}

/**
 * Clear all clickable items above the moves database
 */
function clearMovesLinks()
{
    var movesLink = document.getElementById("movesHistory")

    while(movesLink.firstChild)
    {
        movesLink.removeChild(movesLink.firstChild);
    }
}

/**
 * Handles the move, when it is selected from the clickable items above the moves database,
 * going back or forward on the history, depending on the demanded move index.
 * @param {number} selectedMoveIndex 
 */
function goToPosition(selectedMoveIndex)
{
    // Check if user selected the move corresponding to the current position on the board
    if (selectedMoveIndex == currentMoveIndex -1)
    {
        return
    }

    // Check if the user is trying to go back or forward  
    if (selectedMoveIndex < currentMoveIndex - 1)
    {
        // Trying to go back
        goBack(board, chessKernel, moves, currentMoveIndex - 1 - selectedMoveIndex)
    }
    else
    {
        // Trying to go forward
        goForward(board, chessKernel, moves, selectedMoveIndex + 1 - currentMoveIndex)
    }
}

/**
 * Add css class that highlights the latest move played on the board 
 */
function setHighlightedMove()
{
    var movesLink = document.getElementById("movesHistory");
    movesLink.children[currentMoveIndex - 1].classList.add("current-move");
}

/**
 * Removes css class that highlights the latest move played on the board 
 */
function unsetHighlightedMove()
{
    var movesLink = document.getElementById("movesHistory");
    movesLink.children[currentMoveIndex - 1].classList.remove("current-move");
}