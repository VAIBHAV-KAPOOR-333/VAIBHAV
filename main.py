from fastapi import FastAPI
from models import Register

app=FastAPI()


registration=[
    Register(id=3, name='vk', phone=9876543210, address='mohali'),
    Register(id=1, name='kt', phone=1234567890, address='pkl'),
    Register(id=2, name='kk', phone=1234567890, address='pkl')
]


@app.get("/")
def greet():
    return {"message": "hello world"}


@app.get("/regis")
def reg():
    return registration


@app.get("/regist/{id}")
def get_reg_by_id(id: int):
    for regist in registration:
        if regist.id == id:
            return regist
    return {"error": "not registered id"}


@app.post("/register")
def add_reg(r: Register):
    registration.append(r)
    return r

