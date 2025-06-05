# blog-api
This is a RESTful API for a blogging platform, with authentication, posts, comments, and likes.

Live preview: https://blog-api-p2dq.onrender.com/docs
A user with username ```batman``` and password ```batman123``` is already created. Feel free to use it

### Features
- JWT Auth: For registering and logging in
- Protected routes: You need an access token for certain routes
- Comments: Write comments under a specific post
- Likes: Add/Remove a like from a post

### Tech Stack
- Python, FastAPI, PostgreSQL, OAuth2 for JWT

### Installation

- Clone the repo and cd into the project directory
```bash
git clone https://github.com/Infamous003/blog-api.git
```
- Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
- Install the dependencies
```bash
pip install -r requirements.txt
```
- Start uvicorn server
```bash
uvirorn app:app --reload
```
- Go to http://127.0.0.1:8000/docs
