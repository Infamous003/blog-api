from fastapi import FastAPI, HTTPException, status, Depends
from models import PostCreate, Post, PostUpdate, PostPublic
from database import init_db, get_sesssion
from sqlmodel import select, Session
from contextlib import asynccontextmanager


# This piece of code will make sure that the db is created before we start making requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield



app = FastAPI(
    title="Blog API",
    description="This is a simple blog api",
    lifespan=lifespan)



@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts",
         response_model=list[PostPublic],
         status_code=status.HTTP_200_OK)
def get_posts(session: Session = Depends(get_sesssion)):
    
    query = select(Post)
    posts = session.exec(query).fetchall()

    if not posts:
        return {'message': 'Looks so empty...'}
    return posts


@app.get("/posts/{id}",
         response_model=PostPublic,
         status_code=status.HTTP_200_OK)
def get_posts(id: int, session: Session = Depends(get_sesssion)):
    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()
    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return post_found


@app.post("/posts",
          response_model=PostPublic,
          status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate, session: Session = Depends(get_sesssion)):
    # with Session(engine) as session:
    new_post = Post(**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@app.put("/posts/{id}", response_model=PostPublic, status_code=status.HTTP_200_OK)
def update_posts(id: int, post: PostUpdate, session: Session = Depends(get_sesssion)):
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

@app.delete("/posts/{id}",
            status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, session: Session = Depends(get_sesssion)):

    query = select(Post).where(Post.id == id)
    post_found = session.exec(query).one_or_none()

    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    session.delete(post_found)
    session.commit()