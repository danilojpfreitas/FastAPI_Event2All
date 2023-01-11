from fastapi import FastAPI
import uvicorn
from user.routers import user

app = FastAPI()

@app.get("/")
def home() -> str:
    return "Minha api esta no ar"

app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)