from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://attendance-system-five-red.vercel.app",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # change in production later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# routers
from app.routes import auth_routes, attendance_routes, ai_routes

app.include_router(auth_routes.router)
app.include_router(attendance_routes.router)
app.include_router(ai_routes.router)

# optional router (safe import)
try:
    from app.routes import overtime_routes
    app.include_router(overtime_routes.router)
except Exception:
    print("⚠️ Overtime route not found - skipping")

@app.get("/")
def home():
    return {"message": "Backend is running."}




# from fastapi import FastAPI
# from app.routes import auth_routes, attendance_routes, overtime_routes, ai_routes
# from fastapi.middleware.cors import CORSMiddleware
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# app.include_router(auth_routes.router)
# app.include_router(attendance_routes.router)
# app.include_router(overtime_routes.router)
# app.include_router(ai_routes.router)

# @app.get("/")
# def home():
#     return {"message": "Backend is running."}


