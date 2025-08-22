from fastapi import APIRouter, Depends, status, HTTPException, Request
from models import Post, PostPublic, PostCreate, PostUpdate, User
from sqlmodel import Session, select
from database import get_session
from routes.auth import get_current_user
import json

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/",
         response_model=list[PostPublic],
         status_code=status.HTTP_200_OK)
async def get_posts(request: Request, session: Session = Depends(get_session)):
    redis = request.app.state.redis

    cache = None
    cache = await redis.get("posts")

    if cache is not None:
        decoded = cache.decode()
        posts = json.loads(decoded)
        print("Cache hit!")
        return posts
    else:
        query = select(Post)
        posts = session.exec(query).fetchall()
        if not posts:
            return []
        post_dicts = [post.model_dump(mode="json") for post in posts]
        # mode=json helps us convert dattime objects to strings. without it
        # the datetime objs are not json serializable!
        
        await redis.set("posts", json.dumps(post_dicts), ex=1800) #cache expires after 30 minutes
        print("Cache miss!")
        return posts
    
@router.get("/my-posts",
            response_model=list[PostPublic],
            status_code=status.HTTP_200_OK)
async def get_my_posts(get_current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    my_posts = session.exec(
    select(Post).where(Post.user_id == get_current_user.id)
    ).fetchall()

    return my_posts


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
async def create_posts(post: PostCreate,
                 request: Request,
                 get_current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    redis = request.app.state.redis

    user_id = get_current_user.id
    username = get_current_user.username
    new_post = Post(**post.model_dump())
    new_post.user_id = user_id
    new_post.username = username

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    # Delete the cache and let it build in the next GET request
    # This reduces the complexity of having to manually update the cache
    await redis.delete("posts")
    return new_post


@router.put("/{id}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def update_posts(id: int,
                 post: PostUpdate,
                 request: Request,
                 get_current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    redis = request.app.state.redis
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post_found.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access. You don't have to permission to modify/delete this post")

    if post.title: post_found.title = post.title
    if post.content: post_found.content = post.content
    if post.subtitle: post_found.subtitle = post.subtitle

    session.add(post_found)
    session.commit()
    session.refresh(post_found)

    await redis.delete("posts")
    return post_found

@router.delete("/{id}",
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int,
                 request: Request,
                 get_current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    redis = request.app.state.redis
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post_found.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access. You don't have to permission to modify/delete this post")
    session.delete(post_found)
    session.commit()

    await redis.delete("posts")
