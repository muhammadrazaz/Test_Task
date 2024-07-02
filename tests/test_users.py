import json
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
from app.main import app
from io import StringIO


import pytest



DATABASE_URL = "mysql+pymysql://root:root@localhost/test_db"


engine = create_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

client = TestClient(app)


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown():
    # Begin a new database session
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    # Override get_db to use this session
    app.dependency_overrides[get_db] = lambda: session

    yield

    # Rollback the transaction after the test
    session.close()
    transaction.rollback()
    connection.close()



def test_create_user_with_no_first_name():
    response = client.post("/api/auth/register", json={
        "last_name": "User",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
        
    })
    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "first_name"
      ],
      "msg": "Field required",
      "input": {
        "last_name": "User",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "phone_no": "+1234567890"
      }
    }
  ]
}
    

def test_create_user_with_first_name_too_short():
    response = client.post("/api/auth/register", json={
        "first_name":"t",
        "last_name": "User",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
        
    })
    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "first_name"
      ],
      "msg": "String should have at least 2 characters",
      "input": "t",
      "ctx": {
        "min_length": 2
      }
    }
  ]
}
    

def test_create_user_with_first_name_too_long():
    response = client.post("/api/auth/register", json={
        "first_name":"this is the test with first name too long",
        "last_name": "User",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
        
    })
    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "string_too_long",
      "loc": [
        "body",
        "first_name"
      ],
      "msg": "String should have at most 25 characters",
      "input": "this is the test with first name too long",
      "ctx": {
        "max_length": 25
      }
    }
  ]
}


def test_create_user_with_no_last_name():
    response = client.post("/api/auth/register", json={
        "first_name" : "test",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
        
    })
    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "last_name"
      ],
      "msg": "Field required",
      "input": {
        "first_name": "test",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "phone_no": "+1234567890"
      }
    }
  ]
}
    

def test_create_user_with_last_name_too_short():
    response = client.post("/api/auth/register", json={
        "first_name":"test",
        "last_name": "U",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
        
    })
    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "last_name"
      ],
      "msg": "String should have at least 2 characters",
      "input": "U",
      "ctx": {
        "min_length": 2
      }
    }
  ]
}
    

def test_create_user_with_last_name_too_long():
    response = client.post("/api/auth/register", json={
        "first_name":"test",
        "last_name": "this is the test with last name too long",
        "email": "test11@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
    })
    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "string_too_long",
      "loc": [
        "body",
        "last_name"
      ],
      "msg": "String should have at most 25 characters",
      "input": "this is the test with last name too long",
      "ctx": {
        "max_length": 25
      }
    }
  ]
}
    
def test_create_user_with_no_email():
    response = client.post("/api/auth/register",json={
        "first_name":"test",
        "last_name": "user",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
    })

    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "email"
      ],
      "msg": "Field required",
      "input": {
        "first_name": "test",
        "last_name": "user",
        "password": "Test@1234",
        "confirm_password": "Test@1234",
        "phone_no": "+1234567890"
      }
    }
  ]
}
    
def test_create_user_with_invalid_email():
    response = client.post("/api/auth/register",json={
        "first_name":"test",
        "last_name": "user",
        "email": "test11",
        "password": "Test@1234",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
    })

    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "email"
      ],
      "msg": "value is not a valid email address: An email address must have an @-sign.",
      "input": "test11",
      "ctx": {
        "reason": "An email address must have an @-sign."
      }
    }
  ]
  }
    

def test_create_user_with_no_password():
    response = client.post("/api/auth/register",json={
       "first_name":"test",
        "last_name": "user",
        "email": "test0@gmail.com",
        "confirm_password" : "Test@1234",
        "phone_no": "+1234567890"
    })

    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "password"
      ],
      "msg": "Field required",
      "input": {
        "first_name": "test",
        "last_name": "user",
        "email": "test0@gmail.com",
        "confirm_password": "Test@1234",
        "phone_no": "+1234567890"
      }
    }
  ]
}
    
def test_create_user_with_no_confirm_password():
    response = client.post("/api/auth/register",json={   
        "first_name":"test",
        "last_name": "user",
        "email": "test0@gmail.com",
        "password" : "12345678",
        "phone_no": "+1234567890"
})

    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "confirm_password"
      ],
      "msg": "Field required",
      "input": {
        "first_name": "test",
        "last_name": "user",
        "email": "test0@gmail.com",
        "password": "12345678",
        "phone_no": "+1234567890"
      }
    }
  ]
}

def test_create_user_with_different_confirm_password():
    response = client.post("/api/auth/register",json={   
        "first_name":"test",
        "last_name": "user",
        "email": "test0@gmail.com",
        "password" : "12345678",
        "confirm_password" : "12345679",
        "phone_no": "+1234567890"
})

    assert response.status_code == 422
    assert response.json() == {
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "confirm_password"
      ],
      "msg": "Value error, passwords do not match",
      "input": "12345679",
      "ctx": {
        "error": {}
      }
    }
  ]
}
    

def test_create_user_valid_data():
    response = client.post("/api/auth/register", json={
        "first_name" : "test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234"   
        
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_create_user_with_registered_email():
    response = client.post("/api/auth/register", json={
        "first_name" : "test",
        "last_name": "User",
        "email": "test0@example.com",
        "password": "Test@1234",
        "confirm_password" : "Test@1234"   
        
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


# ======================= Test Cases For Login ======================


def test_login_without_password():
    


    response = client.post('/api/auth/token',
                                    data={'username':'test0@gmail.com'
                                          })
    
    assert response.status_code == 422
    assert response.json() == {
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "password"
            ],
            "msg": "Field required",
            "input": None
        }
    ]
}
    
def test_login_without_username():
    


    response = client.post('/api/auth/token',
                                    data={'password':'12345678'
                                          })
    
    assert response.status_code == 422
    assert response.json() == {
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "username"
            ],
            "msg": "Field required",
            "input": None
        }
    ]
}
    
def test_login_with_invalid_username_and_password():
    


    response = client.post('/api/auth/token',
                                    data={
                                        'username' : 'test@gmail.com',
                                        'password':'1234567'
                                          })
    
    assert response.status_code == 401
    assert response.json()["detail"] == 'Could not validate user'


def test_login_with_valid_username_and_password():
    


    response = client.post('/api/auth/token',
                                    data={
                                        'username' : 'test0@example.com',
                                        'password':'Test@1234'
                                          })
    
    assert response.status_code == 200
    return response.json()["access_token"]


#====================== Test Cases For Update Profiel ======================


def test_update_profile_without_token():
    response = client.patch('/api/update-profile',json={
        "first_name":"test",
        "last_name" : "user",
        "phone_no" :'+12000000000'
    })

    assert response.status_code == 401

def test_update_profie_with_token():
    token = test_login_with_valid_username_and_password()
    response = client.patch('/api/update-profile',headers={"Authorization": f"Bearer {token}"},json={
        "first_name":"updated",
        "last_name" : "user",
        "phone_no" :'+12000000000'
    })

    assert response.status_code == 200


def test_update_profie_with_first_name_too_short():
    token = test_login_with_valid_username_and_password()
    response = client.patch('/api/update-profile',headers={"Authorization": f"Bearer {token}"},json={
        "first_name":"u",
        "last_name" : "user",
        "phone_no" :'+12000000000'
    })

    assert response.status_code == 422

def test_update_profie_with_first_name_too_long():
    token = test_login_with_valid_username_and_password()
    response = client.patch('/api/update-profile',headers={"Authorization": f"Bearer {token}"},json={
        "first_name":"this is the test with first name too long",
        "last_name" : "user",
        "phone_no" :'+12000000000'
    })

    assert response.status_code == 422

def test_update_profie_with_last_name_too_short():
    token = test_login_with_valid_username_and_password()
    response = client.patch('/api/update-profile',headers={"Authorization": f"Bearer {token}"},json={
        "first_name":"updated",
        "last_name" : "u",
        "phone_no" :'+12000000000'
    })

    assert response.status_code == 422

def test_update_profie_with_last_name_too_long():
    token = test_login_with_valid_username_and_password()
    response = client.patch('/api/update-profile',headers={"Authorization": f"Bearer {token}"},json={
        "first_name":"updated",
        "last_name" : "this is the test with first name too long",
        "phone_no" :'+12000000000'
    })

    assert response.status_code == 422

def test_update_profie_with_phone_no_too_short():
    token = test_login_with_valid_username_and_password()
    response = client.patch('/api/update-profile',headers={"Authorization": f"Bearer {token}"},json={
        "first_name":"updated",
        "last_name" : "user",
        "phone_no" :'+120000'
    })

    assert response.status_code == 422

def test_update_profie_with_phone_no_too_long():
    token = test_login_with_valid_username_and_password()
    response = client.patch('/api/update-profile',headers={"Authorization": f"Bearer {token}"},json={
        "first_name":"updated",
        "last_name" : "user",
        "phone_no" :'+12000000000000000'
    })

    assert response.status_code == 422




# ==================== Test Cases For Update Profile Picture =======================

import pkg_resources
from io import BytesIO

def test_update_profile_picture_without_token():
   
    
   
    filename = 'svg.svg'
    
    with open(pkg_resources.resource_filename('tests', filename), 'rb') as img:
        img_bytes_io = BytesIO(img.read())

    img_bytes_io.seek(0)

    response = client.patch('/api/update-profile-picture', 
                        files={"profile_picture": (filename, img_bytes_io, "image/svg+xml")}
                            )
    
    assert response.status_code == 401

def test_update_profile_picture_with_wrong_format():
    token = test_login_with_valid_username_and_password()
    filename = 'svg.svg'
    
    with open(pkg_resources.resource_filename('tests', filename), 'rb') as img:
        img_bytes_io = BytesIO(img.read())

    img_bytes_io.seek(0)

    response = client.patch(
        '/api/update-profile-picture',
        headers={"Authorization": f"Bearer {token}"},
        files={"profile_picture": (filename, img_bytes_io, "image/svg+xml")}
    )
    
 
    assert response.status_code == 400

def test_update_profile_picture_with_correct_format():
    token = test_login_with_valid_username_and_password()
    filename = 'png_img.png'
    
    with open(pkg_resources.resource_filename('tests', filename), 'rb') as img:
        img_bytes_io = BytesIO(img.read())

    img_bytes_io.seek(0)

    response = client.patch(
        '/api/update-profile-picture',
        headers={"Authorization": f"Bearer {token}"},
        files={"profile_picture": (filename, img_bytes_io, "image/png")}
    )
    
 
    assert response.status_code == 200


# =================== Test Cases For Update Password ========================

def test_update_password_with_wrong_old_password():
    token =  test_login_with_valid_username_and_password()

    response = client.patch('/api/update-password',headers={"Authorization": f"Bearer {token}"},
            json={
            "old_password" : 'abc12345',
            "password" : "12345678",
            "confirm_password" : "12345678"
        }
    )


    assert response.status_code == 422

def test_update_password_with_no_password():
    token =  test_login_with_valid_username_and_password()

    response = client.patch('/api/update-password',headers={"Authorization": f"Bearer {token}"},json={
        "old_password" : 'abc12345',
        
        "confirm_password" : "12345678"
    })


    assert response.status_code == 422

def test_update_password_with_different_confirm_password():
    token =  test_login_with_valid_username_and_password()

    response = client.patch('/api/update-password',headers={"Authorization": f"Bearer {token}"},
            json={
            "old_password" : '12345678',
            "password" : "12345678",
            "confirm_password" : "12345679"
        }
    )


    assert response.status_code == 422

def test_update_password_with_valid_data():

    token =  test_login_with_valid_username_and_password()

    response = client.patch('/api/update-password',headers={"Authorization": f"Bearer {token}"},
            json={
            "old_password" : 'Test@1234',
            "password" : "12345678",
            "confirm_password" : "12345678"
        }
    )


    assert response.status_code == 200


# ================== Test Cases For Delete Profile Picture ===========

def test_delete_profile_picture_without_token():
    response = client.delete('/api/profile-picture')
    assert response.status_code == 401


def test_delete_profile_picture_with_token():
    token = test_login_with_valid_username_and_password()
    response = client.delete('/api/profile-picture',headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200


# =================== Test Cases For Delete Phone Number =========================

def test_delete_phone_no_without_token():
    response = client.delete('/api/phone-number')
    assert response.status_code == 401


def test_delete_phone_no_with_token():
    token = test_login_with_valid_username_and_password()
    response = client.delete('/api/phone-number',headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200

