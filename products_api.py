import uvicorn
from fastapi import FastAPI

from routers.product_routes import router as product_router


app = FastAPI()

app.include_router(product_router,prefix="/products", tags=["products"])

if __name__ == "__main__":
    try: uvicorn.run(app,host="0.0.0.0",port=8000)
    except KeyboardInterrupt:
        print("Server is shutting down...")