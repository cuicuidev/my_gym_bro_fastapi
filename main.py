from fastapi import FastAPI

import auth
import sets

app = FastAPI()

app.include_router(router=auth.routes.router)
app.include_router(router=sets.routes.router)

@app.get('/')
async def health():
    return {"status" : "running"}