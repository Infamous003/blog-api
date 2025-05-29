from fastapi import HTTPException, status, Depends, APIRouter
from sqlmodel import select, Session
from database import get_session
from models import User, Post, Comment, CommentCreate, CommentPublic, CommentUpdate
from .auth import get_current_user

router = APIRouter(tags=["Comments"])

@router.get("/comments",
            status_code=status.HTTP_200_OK,
            response_model=list[CommentPublic])
def get_comments(session: Session = Depends(get_session)):
    query = select(Comment)
    comments = session.exec(query).fetchall()

    return comments


@router.get("/posts/{post_id}/comments",
            status_code=status.HTTP_200_OK,
            response_model=list[CommentPublic])
def get_comments(post_id: int,
                 session: Session = Depends(get_session)):
    query = select(Post).where(Post.id == post_id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    query = select(Comment).where(Comment.post_id == post_id)
    comments = session.exec(query).fetchall()
    return comments


@router.post("/posts/{post_id}/comments",
             status_code=status.HTTP_201_CREATED,
             response_model=CommentPublic)
def create_comment(post_id: int,
                   comment: CommentCreate,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    
    query = select(Post).where(Post.id == post_id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    else:
        new_comment = Comment(**comment.model_dump())
        new_comment.post_id = post_id
        new_comment.user_id = current_user.id

        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)

        return new_comment
    
@router.put("/posts/{post_id}/comments/{comment_id}",
            status_code=status.HTTP_200_OK,
            response_model=CommentPublic)
def update_comment(post_id: int,
                   comment_id: int,
                   comment: CommentUpdate,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    
    query = select(Comment).where(Comment.id == comment_id,
                                  Comment.post_id == post_id)
    comment_found = session.exec(query).one_or_none()
    if comment_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if comment_found.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the permission to update this comment")

    comment_found.comment_text = comment.comment_text

    session.add(comment_found)
    session.commit()
    session.refresh(comment_found)
    return comment_found   
    
@router.delete("/posts/{post_id}/comments/{comment_id}",
               status_code=status.HTTP_200_OK)
def delete_comment(post_id: int,
                   comment_id: int,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    
    query = select(Comment).where(Comment.id == comment_id,
                                  Comment.post_id == post_id)
    comment_found = session.exec(query).one_or_none()

    if comment_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if comment_found.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the permission to delete this comment.")
    
    session.delete(comment_found)
    session.commit()