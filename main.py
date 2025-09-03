# FastAPI is a modern, fast (high-performance), web framework for building
# APIs with Python 3.7+ based on standard Python type hints.
from fastapi import FastAPI  # type: ignore # import FastAPI from fastapi module

from routers.user import user_router
from routers.event import event_router
from routers.speaker import speaker_router
from routers.registration import registration_router


# Create an instance of the FastAPI class and assign it to the variable app.
app = FastAPI()



app.include_router(user_router, tags=["Users"], prefix="/users")

app.include_router(event_router, tags=["Events"], prefix="/events")

app.include_router(speaker_router, tags=["Speakers"], prefix="/speakers")

app.include_router(registration_router, tags=["Registration"], prefix="/registration")



# Use the app instance to define a route for the home page.
@app.get("/")
def home():
    return {"message": "Hello Server"}

# See interactive API docs at http://localhost:8000/docs.

