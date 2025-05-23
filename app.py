from fastapi import FastAPI, HTTPException, status
from models import PostCreate, Post

app = FastAPI(title="Blog API", description="This is a simple blog api")

posts = [
    {"id": 1, "title": "First post", "description": "This is a little longer"},
    {"id": 2, "title": "2nd post", "description": "Thidddttle longer"},
    {"id": 3, "title": "Third post", "description": "Tdhis is add little ldonger"},
    {"id": 4, "title": "4th post", "description": "This is dadd little ldonger"},
]


@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    return posts

@app.get("/posts/{id}")
def get_posts(id: int):
    post_found = None
    for post in posts:
        if post.get("id") == id:
            post_found = post
    
    if post_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return post_found 

@app.post("/posts")
def create_posts(post: PostCreate):
    new_post = Post(**post.model_dump(), id=len(posts)+1)
    posts.append(new_post)
    return new_post

@app.put("/posts/{id}")
def update_posts(id: int):
    pass

@app.delete("/posts/{id}")
def delete_posts(id: int):
    for post in posts:
        if post.get("id") == id:
            posts.remove(post)
            return {"message": "Post successfully deleted"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")