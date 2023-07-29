from fastapi import FastAPI

from app.users.router import router as router_users
from app.users_relationships.router_action import router as router_request
from app.users_relationships.router_status import router as router_status

app = FastAPI()
app.include_router(router_users)
app.include_router(router_request)
app.include_router(router_status)


@app.get("/test")
def test():
    return "TEST!"
