from pydantic import BaseModel, HttpUrl


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_url: str
    short_code: str


class URLStatsResponse(BaseModel):
    short_code: str
    original_url: str
    click_count: int
    created_at: str