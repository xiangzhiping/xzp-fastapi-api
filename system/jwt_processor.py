import jwt
from config.constant import AUTHORIZATION_EFFECTIVE_DAYS
from datetime import datetime, timedelta, timezone
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK


class JwtProcessor:

    def __init__(self):
        self.audience: str = "xzp-fast-api"
        self.algorithm: str = "HS256"
        self.key: str = '0cde14c2ehx#42@^&BHF*DF#ERC9fb5e8'
        self.headers: dict[str, str] = {"alg": self.algorithm, "typ": "JWT"}

    async def jwtCipher(self, value: str, effective: bool = True) -> str:
        """jwt加密器"""
        currentTime: datetime = datetime.now(timezone.utc)
        if effective:
            expTime: datetime = currentTime + timedelta(days=AUTHORIZATION_EFFECTIVE_DAYS)
        else:
            expTime: datetime = currentTime - timedelta(days=1)
        payload = {
            "iss": "xzp-fast-api",
            "sub": value,
            "aud": self.audience,
            "exp": expTime,
            "nbf": currentTime,
            "iat": currentTime,
            "jti": "xzp",
        }
        return jwt.encode(payload, self.key, algorithm=self.algorithm, headers=self.headers)

    async def jwtParser(self, authorization: str) -> [int, str, None | str]:
        """jwt解密器"""
        try:
            payload = jwt.decode(
                authorization,
                self.key,
                algorithms=[self.algorithm],
                audience=self.audience
            )
            return HTTP_200_OK, '身份验证成功!', payload.get('sub')
        except jwt.ExpiredSignatureError:
            return HTTP_401_UNAUTHORIZED, '访问凭证已过期, 请重新登录!', 'AUTH_FAILED'
        except jwt.DecodeError:
            return HTTP_401_UNAUTHORIZED, '访问凭证格式和密钥错误, 请重新登录!', 'AUTH_FAILED'
        except jwt.MissingRequiredClaimError:
            return HTTP_401_UNAUTHORIZED, '访问凭证缺少必需的声明, 请重新登录!', 'AUTH_FAILED'
        except jwt.InvalidIssuerError:
            return HTTP_401_UNAUTHORIZED, '访问凭证验证发行者失败, 请重新登录!', 'AUTH_FAILED'
        except jwt.ImmatureSignatureError:
            return HTTP_401_UNAUTHORIZED, '访问凭证尚未生效, 请重新登录!', 'AUTH_FAILED'
        except jwt.InvalidTokenError:
            return HTTP_401_UNAUTHORIZED, '访问凭证校验无效, 请重新登录!', 'AUTH_FAILED'


jp = JwtProcessor()

# async def main():
#     tokenStr = await jp.jwtCipher("7130535699270471680")
#     print(tokenStr)
#     userInfo = await jp.jwtParser(tokenStr)
#     print(userInfo)
#
#
# import asyncio
#
# asyncio.run(main())
