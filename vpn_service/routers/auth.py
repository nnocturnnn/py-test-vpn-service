from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models import User, UserInDB, UpdateUserData
from app.utils import hash_password, verify_password, create_access_token, verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

fake_users_db = {
    "user1": UserInDB(username="user1", hashed_password=hash_password("mypassword"), email="user1@example.com", full_name="User One", phone="123456789"),
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    return user

@router.post("/register", response_model=User)
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = UserInDB(username=user.username, hashed_password=hashed_password)
    return user

@router.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def get_user_data(current_user: UserInDB = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
    }

@router.put("/users/me")
def update_user_data(user_data: UpdateUserData, current_user: UserInDB = Depends(get_current_user)):
    if user_data.email:
        current_user.email = user_data.email
    if user_data.full_name:
        current_user.full_name = user_data.full_name
    if user_data.phone:
        current_user.phone = user_data.phone
    
    fake_users_db[current_user.username] = current_user
    
    return {
        "message": "User data updated successfully",
        "updated_data": {
            "email": current_user.email,
            "full_name": current_user.full_name,
            "phone": current_user.phone,
        }
    }