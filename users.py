from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from database import get_sesssion
from models import UserCreate, UserUpdate, User, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/",
             response_model=UserPublic,
             status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_sesssion)):
    query = select(User).where(User.username == user.username)
    user_found = session.exec(query).one_or_none()

    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username taken')
    else:
        new_user = User(**user.model_dump())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

@router.put("/{id}",
            response_model=UserPublic,
            status_code=status.HTTP_200_OK)
def update_user(id: int, user: UserUpdate, session: Session = Depends(get_sesssion)):
    query = select(User).where(User.id == id)
    user_found = session.exec(query).one_or_none()

    if user_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.username: user_found.username = user.username
    if user.password: user_found.password = user.password

    session.add(user_found)
    session.commit()
    session.refresh(user_found)
    return user_found

@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_sesssion)):
    query = select(User).where(User.id == id)

    user_found = session.exec(query).one_or_none()

    if user_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        session.delete(user_found)
        session.commit()
