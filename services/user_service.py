from schemas.user_schema import UserAuth
from models.user_model import User
from core.security import hash_password

class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        usuario = User(
            username = user.username,
            email = user.email,
            hashed_password = hash_password(user.password)
        )
        await usuario.save()
        return usuario