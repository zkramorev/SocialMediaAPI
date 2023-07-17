from fastapi import FastAPI

from app.users.router import router as router_users


app = FastAPI()
app.include_router(router_users)

@app.get("/test")
def test():
    return "TEST!"