# chess-games-explorer

Flask powered web application that allows a chess player to see all the positions he played in chess.com platform. The games can be filtered by the player rating (e.g. only displays games in which the player rating is above 1800), the time class (e.g. blitz, bullet, rapid, daily) and/or time control (e.g. 300, 900+10, 300+5).

The application also displays the winning, losing and drawing percentages of the games in which each position was reached. It allows the player to track which positions he/she encounters more often, and the positions he/she most struggles with.

The application uses chess.com API to import the games, chessboard.js to embed the chess board and chess.js to handle the moves.

chess.com API:
    https://www.chess.com/news/view/published-data-api

chessboard.js:
    Copyright 2019 Chris Oakman
    https://chessboardjs.com/index.html
    https://github.com/oakmac/chessboardjs

chess.js:
    Copyright (c) 2020, Jeff Hlywa (jhlywa@gmail.com)
    https://github.com/jhlywa/chess.js
    

