# src/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.users import User
from src.api.schemas.auth import LoginRequest, LoginResponse
from src.core.security import verify_password
from src.core.auth import create_access_token

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    # DEBUG: Print the request
    print("=" * 60)
    print(f"🔍 LOGIN ATTEMPT: {request.username}")
    print(f"   Password provided: {request.password}")
    
    # Find user
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user:
        print("User NOT found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    print(f"User found: {user.username}")
    print(f"   User ID: {user.user_id}")
    print(f"   Role: {user.role}")
    print(f"   Stored hash: {user.password}")
    
    # Verify password
    password_valid = verify_password(request.password, user.password)
    print(f"   Password valid: {password_valid}")
    
    if not password_valid:
        print("Password verification FAILED!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    print("Password verification SUCCESS!")
    
    # Create token
    token_data = {
        "sub": str(user.user_id),
        "username": user.username,
        "role": user.role,
        "user_id": user.user_id,
    }
    
    access_token = create_access_token(token_data)
    print("Token created!")
    print("=" * 60)
    
    return LoginResponse(
        access_token=access_token,
        user_id=user.user_id,
        username=user.username,
        role=user.role
    )