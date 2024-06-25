from dataclasses import dataclass

from todoapp.application.auth.interfaces.repository import TokensRepo, TokenKey
from todoapp.application.auth.jwt import JWTAuthenticator
from todoapp.application.common.command import Command, CommandHandler


@dataclass
class DeactivateRefreshToken(Command[None]):
    refresh_token: str


class DeactivateRefreshTokenHandler(CommandHandler[DeactivateRefreshToken, None]):
    repo: TokensRepo
    jwt: JWTAuthenticator

    async def __call__(self, command: DeactivateRefreshToken) -> None:
        refresh_token = self.jwt.decode_refresh_token(command.refresh_token)

        await self.repo.delete_token(TokenKey(
            user_id=refresh_token.user_id,
            refresh_token_id=refresh_token.token_id,
        ))
