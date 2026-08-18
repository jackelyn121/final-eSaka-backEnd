# src/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.users import User
from src.api.schemas.users import UserCreate, UserUpdate, UserResponse
from src.core.security import hash_password
from src.core.rbac import require_role, Role
from src.core.auth import get_current_user

router = APIRouter()


# CREATE USER - ONLY SYSTEM ADMIN
@router.post("/users", response_model=UserResponse, dependencies=[Depends(require_role(Role.SYSTEM_ADMIN))])
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user. Only System Administrators can do this."""
    hashed_password = hash_password(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# GET USER BY ID - Current user or Admin
@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a user by ID. Users can view their own profile; Admins can view any."""
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Allow if user is viewing their own profile OR is System Admin
    if current_user.user_id != user_id and current_user.role != Role.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )
    
    return db_user


# UPDATE USER - Admin only or self
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a user. Users can update their own profile; Admins can update any."""
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Allow if user is updating their own profile OR is System Admin
    if current_user.user_id != user_id and current_user.role != Role.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    # Prevent non-Admins from changing roles of others
    if "role" in user.dict(exclude_unset=True) and current_user.role != Role.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only System Administrators can change user roles"
        )
    
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


# DELETE USER - ONLY SYSTEM ADMIN
@router.delete("/users/{user_id}", dependencies=[Depends(require_role(Role.SYSTEM_ADMIN))])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a user. Only System Administrators can do this."""
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting the last admin
    if db_user.role == Role.SYSTEM_ADMIN:
        admin_count = db.query(User).filter(User.role == Role.SYSTEM_ADMIN).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete the last System Administrator"
            )
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}