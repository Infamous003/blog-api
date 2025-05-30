from fastapi import HTTPException, status, Depends, APIRouter
from sqlmodel import select, Session
from database import get_session
from models import User, Like
from .auth import get_current_user
from utils import get_post_or_404

router = APIRouter(prefix="/posts", tags=["Likes"])

@router.post("/{post_id}/like")
def like_post(post_id: int,
         current_user: User = Depends(get_current_user),
         session: Session = Depends(get_session)):
    
    post = get_post_or_404(post_id)
    
    query = select(Like).where(Like.post_id == post.id,
                           Like.user_id == current_user.id)
    like_found = session.exec(query).one_or_none()

    if like_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already liked this post")
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        session.add(like)
        session.commit()
    return {"msg": "You liked the post"}

@router.delete("/{post_id}/like")
def unlike_post(post_id: int,
                current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    
    post = get_post_or_404(post_id)
    query = select(Like).where(Like.post_id == post.id,
                               Like.user_id == current_user.id)
    like_found = session.exec(query).one_or_none()

    if like_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have to like a post to unlike it")
    session.delete(like_found)
    session.commit()
    return {"msg": "You unliked the post"}