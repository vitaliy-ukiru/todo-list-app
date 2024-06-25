from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Any
from uuid import UUID

import uuid6
from jwt import PyJWTError, ExpiredSignatureError

from todoapp.application.auth.exceptions import InvalidToken, ExpiredToken
from todoapp.domain.user.entities import UserId

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


@dataclass(frozen=True)
class BaseToken(ABC):
    user_id: UserId
    token_id: str
    raw: str

    @property
    @abstractmethod
    def type(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class RefreshToken(BaseToken):
    @property
    def type(self):
        return REFRESH_TOKEN_TYPE


@dataclass(frozen=True)
class AccessToken(BaseToken):
    @property
    def type(self):
        return ACCESS_TOKEN_TYPE


class JWTAuthenticator(ABC):
    def __init__(
        self,
        access_token_expires: timedelta,
        refresh_token_expires: timedelta,
    ):
        self._access_expires = access_token_expires
        self._refresh_expires = refresh_token_expires

    @abstractmethod
    def _encode(self, payload: dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    def _decode(self, token: str, verify_exp: bool) -> dict[str, Any]:
        raise NotImplementedError

    def _create_token(self, expire: timedelta, token_type: str, **claims) -> str:
        now = datetime.utcnow()
        claims_ = claims.copy()

        claims_.update(iat=now, exp=now + expire, type=token_type)
        return self._encode(claims_)

    def create_access_token(
        self,
        user_id: UserId,
    ) -> AccessToken:
        token_id = str(uuid6.uuid7())

        token = self._create_token(
            self._access_expires,
            ACCESS_TOKEN_TYPE,
            sub=str(user_id),
            jti=token_id,
        )

        return AccessToken(
            token_id=token_id,
            user_id=user_id,
            raw=token
        )

    def create_refresh_token(self, user_id: UserId) -> RefreshToken:
        token_id = str(uuid6.uuid7())
        token = self._create_token(
            self._refresh_expires,
            REFRESH_TOKEN_TYPE,
            sub=str(user_id),
            jti=token_id,
        )
        return RefreshToken(
            token_id=token_id,
            user_id=user_id,
            raw=token
        )

    def _decode_token(self, token: str, expected_type: str, verify_exp: bool) -> dict[str, Any]:
        try:
            payload = self._decode(token, verify_exp)
        except ExpiredSignatureError:
            raise ExpiredToken()
        except PyJWTError as err:
            raise InvalidToken() from err

        token_type = payload.pop("type", None)
        if token_type is None:
            raise InvalidToken()

        if token_type != expected_type:
            raise ValueError(
                f"Expected {expected_type} but got {token_type}")  # TODO: replace with custom exception

        return payload

    def decode_access_token(self, token: str, verify_expiration: bool = True) -> AccessToken:
        payload = self._decode_token(token, ACCESS_TOKEN_TYPE, verify_expiration)
        return AccessToken(
            user_id=UserId(UUID(payload["sub"])),
            token_id=payload["jti"],
            raw=token
        )

    def decode_refresh_token(self, token: str) -> RefreshToken:
        payload = self._decode_token(token, REFRESH_TOKEN_TYPE, True)
        return RefreshToken(
            user_id=UserId(UUID(payload["sub"])),
            token_id=payload["jti"],
            raw=token
        )
