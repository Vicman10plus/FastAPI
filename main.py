from fastapi import FastAPI
from routers import products, users, basic_auth_users

app = FastAPI()


app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)


@app.get("/")
async def root():
    return "Hello FastAPI!"
