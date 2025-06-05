from fastapi import HTTPException, status, Depends, APIRouter, Request
from sqlmodel import select, Session
from database import get_session
from models import User, Comment, CommentCreate, CommentPublic, CommentUpdate
from .auth import get_current_user
from utils import get_post_or_404, get_comment_or_404
import json

router = APIRouter(tags=["Comments"])

@router.get("/comments",
            status_code=status.HTTP_200_OK,
            response_model=list[CommentPublic])
async def get_comments(request: Request,
                 session: Session = Depends(get_session)):
    
    redis = request.app.state.redis

    cache = None
    cache = await redis.get("comments")

    if cache is not None:
        decoded = cache.decode()
        comments = json.loads(decoded)
        return comments
    else:
        query = select(Comment)
        comments = session.exec(query).fetchall()

        comment_dicts = [comment.model_dump(mode="json") for comment in comments]
        await redis.set("comments", json.dumps(comment_dicts), ex=1800)
        return comments


@router.get("/posts/{post_id}/comments",
            status_code=status.HTTP_200_OK,
            response_model=list[CommentPublic])
async def get_comments_for_post(post_id: int,
                            request: Request,
                            session: Session = Depends(get_session)):
    post = get_post_or_404(post_id)
    redis = request.app.state.redis

    cache = None
    cache = await redis.get("comments_for_post")

    if cache is not None:
        decoded = cache.decode()
        comments = json.loads(decoded)
        print(comments)
        return comments
    else:
        query = select(Comment).where(Comment.post_id == post.id)
        comments = session.exec(query).fetchall()
        
        comment_dicts = [comment.model_dump(mode="json") for comment in comments]
        await redis.set("comments_for_post", json.dumps(comment_dicts), ex=1800)
        return comments


@router.post("/posts/{post_id}/comments",
             status_code=status.HTTP_201_CREATED,
             response_model=CommentPublic)
def create_comment(post_id: int,
                   comment: CommentCreate,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    
    post = get_post_or_404(post_id)
    
    new_comment = Comment(**comment.model_dump())
    new_comment.post_id = post.id
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

    comment_found = get_comment_or_404(comment_id, post_id)

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
    
    comment_found = get_comment_or_404(comment_id, post_id)

    if comment_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if comment_found.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the permission to delete this comment.")
    
    session.delete(comment_found)
    session.commit()