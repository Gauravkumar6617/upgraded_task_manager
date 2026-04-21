from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from db.session import engine, Base
from routers import tasks, system
from core.rate_limiter import limiter

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Professional Task Manager")

# ----------------------------
# slowapi setup (no Redis/startup needed)
# ----------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ----------------------------
# Routers
# ----------------------------
app.include_router(tasks.router)
app.include_router(system.router)

# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/")
def root():
    return {"message": "lets go 🚀"}