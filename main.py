from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Dict

app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory database
database: Dict[int, str] = {}
next_id = 1

# Create item
@app.post("/items/")
async def create_item(data: str = Form(...)):
    global next_id
    database[next_id] = data
    next_id += 1
    return RedirectResponse("/", status_code=303)

# Update item
@app.put("/items/{item_id}")
async def update_item(item_id: int, data: str = Form(...)):
    if item_id in database:
        database[item_id] = data
        return RedirectResponse("/", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id in database:
        del database[item_id]
        return RedirectResponse("/", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Serve HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": database})
