from typing import Annotated, Union
from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import DB
from move import move

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = DB()
m = move()
templates.env.globals["cell_status"] = db.get_cell_status
templates.env.globals["is_ship"] = m._isShip


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "side: Player 1"})

@app.get("/player1", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "side: Player 1", "player": 0})

@app.get("/player2", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "side: Player 2", "player": 1})

@app.get("/board/{coord_x}/{coord_y}/{player}", response_class=HTMLResponse)
async def index(coord_x: int, coord_y: int, player:int, request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    print(coord_x, coord_y)
    m.shot(player, coord_x, coord_y)
    # opponent = (player + 1) % 2
    # print(opponent)

    # current_cell = board.cell_with(coord_x=coord_x, coord_y=coord_y)
    # previous_cell = log.pop() if log else None

    # if board.move(previous_cell, current_cell):
    #     cells_to_move = []
    # else:
    #     log.append(current_cell)
    #     cells_to_move = board.can_move_from(cell=current_cell)


    # if hx_request:
    #     return templates.TemplateResponse(
    #         request=request, name="board.html", context={"board": board, "highlighted": cells_to_move}
    #     )
    return  templates.TemplateResponse("table.html", {"request": request, "player": player, "mode": 0}) #JSONResponse(content=jsonable_encoder(board))

@app.get("/newgame", response_class=HTMLResponse)
async def newgame(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    m.newgame()

    # current_cell = board.cell_with(coord_x=coord_x, coord_y=coord_y)
    # previous_cell = log.pop() if log else None

    # if board.move(previous_cell, current_cell):
    #     cells_to_move = []
    # else:
    #     log.append(current_cell)
    #     cells_to_move = board.can_move_from(cell=current_cell)


    # if hx_request:
    #     return templates.TemplateResponse(
    #         request=request, name="board.html", context={"board": board, "highlighted": cells_to_move}
    #     )
    return  templates.TemplateResponse("index.html", {"request": request}) #JSONResponse(content=jsonable_encoder(board))

@app.get("/setships")
async def set_ship():
    pass
