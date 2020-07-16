# Overview

This repo constains the code for a Flask powered web application that allows a chess player to see all the positions he played online in the [chess.com](https://www.chess.com/) platform. The games can be filtered by the player rating (e.g. only displays games in which the player rating is above 1800), the time class (e.g. blitz, bullet, rapid, daily) and/or time control (e.g. 300, 900+10, 300+5).

The application also displays the winning, losing and drawing percentages of the games in which each position was reached. It allows the player to track which positions he/she encounters more often, and the positions he/she most struggles with.

The application uses chess.com API to import the games information, chessboard.js to embed the chess board and chess.js to handle the moves.

You can check it out at http://fer123a.pythonanywhere.com/

NOTE: There is also an integration with the Lichess platform, using its API. However, I don't recommend using it since importing games from Lichess takes waaaaay too much time.

# How to use it

## Home Page

On the home page, type a username from chess.com and select which games you want to see, the ones in which the player plays as white, or the ones in which he plays as black.

If you wish to further filter the games, click on "Filtering Options". It opens a menu, where you can add a filter by "Rating", this way, only the games in which the player has a rating larger than the inserted value will be displayed. 

Another option is to add a "Time Class" filter, where you can select if you want to see "daily", "rapid", "blitz" or "bullet" games. There is also a "Time Control" filter, where you must insert a specific time control, given in seconds. For example, if you wish to see only the games where the players start with 5 minutes and have an increment of 5 seconds for each move (5|5), you must type "300+5". Other examples: 3|2 becomes 180+2; 15|10 becomes 900+10; 5|0 becomes 300.

The filters "Time Control" and "Time Class" don't work together, you can use one of them, but not both.

After all options are set, click on "Search Games".

It may take a while to apply the filters and parse the pgn files, depending on the resulting number of games. 

## Explorer

When all the games are parsed, the explorer page is loaded.

The explorer page is really straight forward. The box on the right side displays the database parsed. You can select a move from it, or drag a piece on the board. After there is a move on the board, you can use the arrows (from the keyboard, or clicking on the buttons) to go back or forward on the position. Be aware that if you go back and change a move, you can't get to that position again using the arrows.

You can also click the reset button to go to the initial position and clicking on the logo takes you back to Home Page.

# Credits

chess.com API:
    https://www.chess.com/news/view/published-data-api

chessboard.js:
    Copyright 2019 Chris Oakman
    https://chessboardjs.com/index.html
    https://github.com/oakmac/chessboardjs

chess.js:
    Copyright (c) 2020, Jeff Hlywa (jhlywa@gmail.com)
    https://github.com/jhlywa/chess.js
    
lichess API:
    https://lichess.org/api
    

