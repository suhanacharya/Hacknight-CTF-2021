from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from deta import Deta
import string
import random
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_KEY = os.getenv("PROJECT_KEY")
print(PROJECT_KEY)

deta = Deta(PROJECT_KEY)
db = deta.Base("flag_db")

origins = [
    "https://273zfa.deta.dev/",
    "https://ctf-hacknight.deta.dev/",
    "http://127.0.0.1:8000/",
    "127.0.0.1:8000"
]

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

file_path = "openme.txt"

# @app.get("/")
# def hello():
#     return {'data': 'hello traveller, you have found the API! But what can you do with this?'}


# @app.get("/home", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("item.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/get/encoded")
def get_encode():
    return FileResponse(path=file_path, filename=file_path, media_type='text/txt')

    # return {"instructions": "Now that you've done something with base64, just take this base64 encoded data and paste it into the input box and click on submit to get the next clue!", "data": img_data}


@app.get("/check/language", tags=["check"])
def check_language(lang, langop):
    if lang.lower() == "brainfuck" and langop.lower() == "hello world":
        return JSONResponse({"data": "POG! U got this!", "res": "https://ctf-hacknight.deta.dev/challenge/encode"})
    else:
        return JSONResponse({"data": "Not POG", "res": False})


@app.get("/check/love", tags=["check"])
def check_love(msg):
    if msg.lower() == "lvhcktbrfst<3":
        return JSONResponse({"data": "POG!", "res": "https://ctf-hacknight.deta.dev/challenge/rps"})
    else:
        return JSONResponse({"data": "unPOG!", "res": False})


# @app.get("/check/dev", tags=["check"])
# def check_dev(msg):
#     if msg.lower() == "beta" or msg.lower() == "beta testing":
#         return {"data": "POG!", "res": "next-challenge"}
#     else:
#         return {"data": "unPog!", "res": False}


@app.get("/check/dev", tags=["check"])
def check_net(msg):
    if msg.lower() == "beta-testing" or "beta" in msg.lower():
        return {"data": "POG!", "res": "https://ctf-hacknight.deta.dev/challenge/network"}
    else:
        return {"data": "unPOG!", "res": False}


@app.get("/check/network", tags=["check"])
def check_net(msg):
    if msg.lower() == "router":
        return {"data": "POG!", "res": "https://ctf-hacknight.deta.dev/challenge/difference"}
    else:
        return {"data": "unPOG!", "res": False}


# @app.get("/check/difference", tags=["check"])
# def check_net(msg):
#     if msg.lower() == "router":
#         return {"data": "POG!", "res": "next-challenge"}
#     else:
#         return {"data": "unPOG!", "res": False}
#     pass


@app.get("/challenge/encode", tags=["challenge"],  response_class=HTMLResponse)
def encode_challenge(request: Request):
    return templates.TemplateResponse("encode_challenge.html", {"request": request})


@app.get("/challenge/language", tags=["challenge"], response_class=HTMLResponse)
def language_challenge(request: Request):
    return templates.TemplateResponse("language_challenge.html", {"request": request})


@app.get("/challenge/love", tags=["challenge"], response_class=HTMLResponse)
def love_challenge(request: Request):
    return templates.TemplateResponse("love_challenge.html", {"request": request})


@app.get("/challenge/dev", tags=["challenge"],  response_class=HTMLResponse)
def dev_challenge(request: Request):
    return templates.TemplateResponse("development_challenge.html", {"request": request})


@app.get("/challenge/network", tags=["challenge"], response_class=HTMLResponse)
def network_challenge(request: Request):
    return templates.TemplateResponse("network_challenge.html", {"request": request})


@app.get("/challenge/difference", tags=["challenge"], response_class=HTMLResponse)
def difference_challenge(request: Request):
    return templates.TemplateResponse("difference_challenge.html", {"request": request})


@app.get("/challenge/memory", tags=["challenge"], response_class=HTMLResponse)
def memory_challenge(request: Request):
    return templates.TemplateResponse("memory_challenge.html", {"request": request})


@app.get("/challenge/rps", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("rps_challenge.html", {"request": request})


@app.get("/challenge/invaders", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("invader_challenge.html", {"request": request})


@app.get("/get/flag")
def gen_flag():
    res = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=10))
    db.insert({}, key=res)

    return {"data": "success!", "flag": res}


@app.get("/verify/flag")
def verify(username, flag):
    print(username, flag)
    check = db.get(flag)

    print(check)
    if check:
        db.update({"username": username}, key=flag)
        return {"data": "Success!", "res": True}
    else:
        return {"data": "Sorry, that's not right :(", "res": False}


@app.get("/leaderboard", response_class=HTMLResponse)
def leaderboard(request: Request):
    li = db.fetch().items
    # if not li:
    #     li = []
    li = li[::-1]
    print(li)
    return templates.TemplateResponse("leaderboard.html", {"request": request, "li":li})

