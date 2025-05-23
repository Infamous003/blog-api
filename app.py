from fastapi import FastAPI

app = FastAPI(title="Blog API", description="This is a simple blog api")

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    pass

@app.get("/posts/{id}")
def get_posts(id: int):
    pass

@app.post("/posts")
def create_posts():
    pass

@app.put("/posts/{id}")
def update_posts(id: int):
    pass

@app.delete("/posts/{id}")
def delete_posts(id: int):
    pass

