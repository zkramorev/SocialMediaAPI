from fastapi import FastAPI

from app.users.router import router as router_users
from app.users_relationships.router import router as router_request


app = FastAPI()
app.include_router(router_users)
app.include_router(router_request)

@app.get("/test")
def test():
    return "TEST!"