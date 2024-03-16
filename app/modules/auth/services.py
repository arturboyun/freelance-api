from fastapi.security import OAuth2PasswordRequestForm
from app.core.uow.uow_base import IUoW
from app.modules.auth.schemes import TokensPair
from app.modules.users.schemes import UserCreate
from app.core.security import security_manager


class AuthService:
    async def register(self, uow: IUoW, user: UserCreate) -> TokensPair:
        """
        Register a new user.

        **Parameters**

        * `uow`: Unit of Work
        * `user`: UserDB

        **Returns**

        * `UserDB`
        """
        async with uow:
            user.password = security_manager.get_password_hash(
                user.password
            )
            if await uow.auth_repo.get_by_username(user.username):
                raise ValueError("User already exists with this username")
            user = await uow.auth_repo.create(user)
            await uow.commit()
            await uow.session.refresh(user)

            access_token = security_manager.create_access_token(
                data={"sub": user.username}
            )
            refresh_token = security_manager.create_refresh_token(
                data={"sub": user.username}
            )
            return TokensPair(access_token=access_token, refresh_token=refresh_token)

    async def login(self, uow: IUoW, login: OAuth2PasswordRequestForm) -> TokensPair:
        """
        Login a user.

        **Parameters**

        * `uow`: Unit of Work
        * `username`: str
        * `password`: str

        **Returns**

        * `UserDB`
        """
        async with uow:
            user = await uow.auth_repo.get_by_username(login.username)
            if not user:
                raise ValueError("User not found")
            if not security_manager.verify_password(login.password, user.password):
                raise ValueError("Incorrect password")
            access_token = security_manager.create_access_token(data={"sub": user.username})
            refresh_token = security_manager.create_refresh_token(data={"sub": user.username})
            return TokensPair(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, uow: IUoW, refresh_token: str) -> TokensPair:
        """
        Refresh the access token.

        **Parameters**

        * `uow`: Unit of Work
        * `refresh_token`: str

        **Returns**

        * `UserDB`
        """
        async with uow:
            try:
                payload = security_manager.decode_token(refresh_token)
                if not payload:
                    raise ValueError("Invalid token")
                username: str = payload.get("sub", None)
                if not username:
                    raise ValueError("Invalid token")
                user = await uow.auth_repo.get_by_username(username)
                if not user:
                    raise ValueError("User not found")
                access_token = security_manager.create_access_token(data={"sub": user.username})
                refresh_token = security_manager.create_refresh_token(data={"sub": user.username})
                return TokensPair(access_token=access_token, refresh_token=refresh_token)
            except Exception as e:
                raise ValueError(str(e))

def get_auth_service() -> AuthService:
    return AuthService()
