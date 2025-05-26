from fastapi import APIRouter, Depends, status, HTTPException
from models import Post, PostPublic, PostCreate, PostUpdate, User
from sqlmodel import Session, select
from database import get_session
from auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/",
         response_model=list[PostPublic],
         status_code=status.HTTP_200_OK)
def get_posts(session: Session = Depends(get_session)):
    
    query = select(Post)
    posts = session.exec(query).fetchall()

    if not posts:
        return {'message': 'Looks so empty...'}
    return posts


@router.get("/{id}",
         response_model=PostPublic,
         status_code=status.HTTP_200_OK)
def get_posts(id: int, session: Session = Depends(get_session)):
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()
    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return post_found


@router.post("/",
          response_model=PostPublic,
          status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate,
                 get_current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    user_id = get_current_user.id
    new_post = Post(**post.model_dump())
    new_post.user_id = user_id
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=PostPublic, status_code=status.HTTP_200_OK)
def update_posts(id: int, post: PostUpdate, session: Session = Depends(get_session)):
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.title: post_found.title = post.title
    if post.description: post_found.description = post.description

    session.add(post_found)
    session.commit()
    session.refresh(post_found)
    return post_found

@router.delete("/{id}",
            status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, session: Session = Depends(get_session)):

    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    session.delete(post_found)
    session.commit()