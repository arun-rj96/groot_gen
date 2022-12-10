import pyqrcode
import uvicorn
from fastapi import FastAPI, Request, Form
import png
import string
import random
from fastapi.responses import HTMLResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static/", StaticFiles(directory="static"), name="static")

AUT_TOKEN = None
REQUEST_AUT_TOKEN = None
SYMBOLS = "@!$*"

def read_root():
    return {"Hello": "World"}

@app.get("/create_qr/")
def create_qr(request:Request):
    global AUT_TOKEN
    AUT_TOKEN = create_aut_token()
    url = pyqrcode.create("http:127.0.0.1:8080/authenticate/" + AUT_TOKEN)
    print(AUT_TOKEN,"flage12")
    url.png("static/images/qr.png", scale = 6)
    return templates.TemplateResponse("qr_page.html",{"request": request,})

@app.get("/authenticate/{aut_token}")
def authenticate(request:Request,aut_token:str):
    global REQUEST_AUT_TOKEN
    REQUEST_AUT_TOKEN = aut_token
    return templates.TemplateResponse("home.html",{"request": request})


@app.post("/validate/")
async def show_success_page(request:Request):
    global AUT_TOKEN
    global REQUEST_AUT_TOKEN
    if AUT_TOKEN != REQUEST_AUT_TOKEN:
        return templates.TemplateResponse("error_page.html",{"request": request})
    form = await request.form()
    if form['user_name'] == "arun@gmail" and form['password'] == "12":
        return templates.TemplateResponse("success.html",{'request':request})
    else:
        return templates.TemplateResponse("faliure.html",{"request": request})

def create_aut_token():
    auth_token = ""
    global SYMBOLS
    for i in range(10):
        auth_token += random.choice(string.ascii_letters)
        auth_token += str(random.randint(0,9))
        auth_token += random.choice(SYMBOLS)
    return auth_token



if __name__ == "__main__":
    uvicorn.run('app:app', host="127.0.0.1", port=8080, workers=1)
    
