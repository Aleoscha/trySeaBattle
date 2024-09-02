from typing import Annotated, Union
from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import DB
from move import move, log

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = DB()
m = move()
templates.env.globals["cell_status"] = db.get_cell_status
templates.env.globals["is_ship"] = m._isShip


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "side: Player 1", "player": 0})

@app.get("/game/{player}/", response_class=HTMLResponse)
async def read_root(player: int, request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Режим боя", "player": player})


@app.get("/board/{coord_x}/{coord_y}/{player}", response_class=HTMLResponse)
async def index(coord_x: int, coord_y: int, player:int, request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    # print(coord_x, coord_y)
    m.shot(player, coord_x, coord_y)
    return  templates.TemplateResponse("table.html", {"request": request, "player": player, "mode": 0}) #JSONResponse(content=jsonable_encoder(board))

@app.get("/newgame", response_class=HTMLResponse)
async def newgame(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    m.newgame()

    return  templates.TemplateResponse("index.html", {"request": request}) #JSONResponse(content=jsonable_encoder(board))


@app.get("/setship/{coord_x}/{coord_y}/{player}", response_class=HTMLResponse)
async def setship(coord_x: int, coord_y: int, player:int, request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    # print(coord_x, coord_y)

    current_cell = (player, coord_x, coord_y)
    previous_cell = log[player].pop() if log[player] else None

    if previous_cell is not None:
      m.addShip(current_cell, previous_cell)
    else:
        log[player].append(current_cell)

    # if board.move(previous_cell, current_cell):
    #     cells_to_move = []
    # else:
    #     log.append(current_cell)
    #     cells_to_move = board.can_move_from(cell=current_cell)

    # if hx_request:
    #     return templates.TemplateResponse(
    #         request=request, name="board.html", context={"board": board, "highlighted": cells_to_move}
    #     )
    return  templates.TemplateResponse("setTable.html", {"request": request, "player": player, "mode": 0})

@app.get("/setShips/{player}/", response_class=HTMLResponse)
async def read_root(player:int, request: Request):
    return templates.TemplateResponse("setShips.html", {"request": request, "message": "Режим расстановки кораблей", "player": player})