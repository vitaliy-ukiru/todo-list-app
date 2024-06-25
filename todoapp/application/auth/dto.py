from todoapp.application.common.dto import DTO


class Tokens(DTO):
    refresh_token: str
    access_token: str
