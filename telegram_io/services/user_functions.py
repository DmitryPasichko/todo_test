import os
import redis
import aiohttp
from telegram_io.dtos import ProfileDto


GET_TOKEN_URL = "/api/v1/token/"
USER_URL = "/shop/user/"

rc = redis.Redis()


def get_base_url():
    return os.getenv("BASE_URL")


class AuthorizationMixin:
    ADMIN_TOKEN_KEY: str = "admin_key"

    async def get_user_token(self, login: str, password: str, redis_key: str) -> str:
        token = self.__get_token_redis(redis_key)

        if not token:
            token = await self.__get_token_api(login, password)
            if token:
                self.__set_token_redis(redis_key, token)
        return token

    @staticmethod
    def __get_token_exp_time() -> int:
        value = os.getenv("ACCESS_TOKEN_LIFETIME_SECONDS")
        return int(value) if value else 3600

    @staticmethod
    async def __get_token_api(login: str, password: str) -> str:
        url = get_base_url() + GET_TOKEN_URL
        token = ""
        data = {
            "username": login,
            "password": password,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status in [200, 201]:
                    access_token = await response.json()
                    token = f"Bearer {access_token.get('access', '')}"
        return token

    @staticmethod
    def __get_token_redis(key: str) -> str:
        value = rc.get(key)
        return value.decode("utf-8") if value else ""

    def __set_token_redis(self, key: str, token: str) -> None:
        rc.set(key, token, ex=self.__get_token_exp_time())


class AdminApiSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AdminApi(AuthorizationMixin, metaclass=AdminApiSingleton):
    ADMIN_TOKEN_KEY: str = "admin_key"

    async def get_user_by_phone(self, phone: str) -> ProfileDto | None:
        result = await self.__get_user_by_phone_or_ext_id("phone", phone)
        return result

    async def get_user_by_external_id(self, external_id) -> ProfileDto | None:
        result = await self.__get_user_by_phone_or_ext_id("external_id", external_id)
        return result

    async def create_new_user(self, profile: ProfileDto):
        headers = await self.__get_headers()
        data = profile.dict()
        url = get_base_url() + USER_URL
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status in [200, 201]:
                    resp = await response.json()
                    profile.id = resp.get("id")

    async def get_profile_balance_by_external_id(self, external_id: str) -> float:
        user = await self.get_user_by_external_id(external_id)
        if user:
            return user.balance.amount
        else:
            return 0.00

    async def is_user_exists(self, external_id: str) -> bool:
        if await self.get_user_by_external_id(external_id):
            return True
        return False

    async def __get_user_by_phone_or_ext_id(self, key, value) -> ProfileDto:
        result = None
        headers = await self.__get_headers()
        url = get_base_url() + USER_URL + f"?{key}={value}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status in [200, 201]:
                    resp = await response.json()
                    if len(resp) >0:
                        result = ProfileDto(**resp[0])
        return result

    async def __get_token(self) -> str:
        return await self.get_user_token(
            os.getenv("BACKEND_LOGIN"),
            os.getenv("BACKEND_PASSWORD"),
            self.ADMIN_TOKEN_KEY,
        )

    async def __get_headers(self) -> dict:
        token = await self.__get_token()
        return {
            "Authorization": token
        }


class UserApi(AuthorizationMixin):
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
        self.redis_token_key = f"token_{login}"

    async def get_token(self) -> str:
        return await self.get_user_token(
            self.login, self.password, self.redis_token_key
        )
