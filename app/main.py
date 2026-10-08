from fastapi import FastAPI

from app.api.customer import router as customer_router
from app.api.risk import router as risk_router
from app.api.support import router as support_router


app = FastAPI(
    title="AI Banking Support & Resolution Platform",
    version="1.0.0"
)

app.include_router(customer_router)
app.include_router(risk_router)
app.include_router(support_router)


@app.get("/")
def root():
    return {
        "message": "AI Banking Support & Resolution Platform is running"
    }