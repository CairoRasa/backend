import dotenv
dotenv.load_dotenv(verbose=True)
from db.FoodItem import FoodItem
import uvicorn, os, routes.manage_items, routes.orders, routes.manage_orders, routes.items
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import User, db, Order
from schemas import UserCreate, UserRead, UserUpdate
from users import auth_backend, fastapi_users

origins = [
    os.getenv("FRONTEND_URL")
]

app = FastAPI(title="CairoRasa API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# logging.info("Starting CairoRasa API...")
# logging.info(f"Cors origins: {origins}")

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(deps.remove_fields_create)],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(routes.manage_items.router)
app.include_router(routes.orders.router)
app.include_router(routes.manage_orders.router)
app.include_router(routes.items.router)


# @app.get("/authenticated-route")
# async def authenticated_route(user: User = Depends(current_active_user)):
#     return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,  # type: ignore
            FoodItem,
            Order.Order
        ],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info", port=int(os.getenv("SERVER_PORT", 4490)))
