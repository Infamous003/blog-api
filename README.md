# Blog API

This is a **RESTful API** for a blogging platform, featuring user authentication, posts, comments, and likes.

## Live docs

Check out the swagger docs here:
https://blog-api-1i1j.onrender.com/docs

Or if you prefer a good UI (build with ReactJS and WebTUI):
https://majestic-croquembouche-a1c89c.netlify.app/

You can log in using the test credentials:

- **Username**: `testuser`  
- **Password**: `password123`

Or create a new user.

## Features

- **JWT Authentication** - Register and log in using jwt tokens
- **Protected Routes** - Access posts, comments, and likes only with a valid jwt token
- **Comments & Likes** - Like/Unlike and post comments under a specific posts

## Tech Stack

- **Python** / **FastAPI**  
- **PostgreSQL**  
- **Docker**
- **JWT Auth**
