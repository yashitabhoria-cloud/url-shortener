from pydantic import BaseModel, HttpUrl, Field


class ShortenRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = Field(default=None, min_length=3, max_length=30)


class ShortenResponse(BaseModel):
    short_url: str
    short_code: str


class URLStatsResponse(BaseModel):
    short_code: str
    original_url: str
    click_count: int
    created_at: str