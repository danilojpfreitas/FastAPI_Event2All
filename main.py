from fastapi import FastAPI
import uvicorn
import psycopg2

from shared.database import Base, engine
from user.routers import user

from user.models.get_user import UserResponseModel

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", tags=["Test"])
def home() -> str:
    return "API Running"

app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)