
from httpx import AsyncClient

import pytest
@pytest.mark.parametrize("email,password,user_name,status_code",
                         [("test@test.com","test","test_user",200), 
                          ("test@test.com","test0","test_user1",409),
                          ("abcd","test2","test_user2",422),
                          ])
async def test_register_user(email, password, user_name, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
        "user_name": user_name  
    })
    assert response.status_code == status_code

@pytest.mark.parametrize("email,password,user_name,status_code",
                         [("test1@test.com","test","test_user_1",200), 
                          ("test@test.com","test0","test_user1",401),
                          ])
async def test_login_user(email, password, user_name, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
        "user_name": user_name  
    })
    assert response.status_code == status_code