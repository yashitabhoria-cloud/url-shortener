from fastapi import FastAPI, HTTPException, Request, Depends, Query
from fastapi.responses import RedirectResponse

from schemas import ShortenRequest, ShortenResponse, URLStatsResponse, UpdateURLRequest, URLListResponse
from sqlite_storage import SQLiteURLRepository
from services import (
    URLShortenerService,
    InvalidShortCodeError,
    ShortCodeAlreadyExistsError,
    InvalidExpirationError,
    ExpiredShortCodeError,
    ShortCodeNotFoundError,
)
from database import initialize_database


app = FastAPI()


initialize_database()

repository = SQLiteURLRepository()
service = URLShortenerService(repository)


def get_url_shortener_service() -> URLShortenerService:
    return service


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(
    request_data: ShortenRequest,
    request: Request,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    try:
        short_code = url_service.create_short_url(
            str(request_data.url),
            request_data.custom_code,
            request_data.expires_at,
        )
    except InvalidShortCodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid custom short code",
        )
    except ShortCodeAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Custom short code already exists",
        )
    except InvalidExpirationError:
        raise HTTPException(
            status_code=400,
            detail="Expiration time must be in the future",
        )

    short_url = str(request.base_url) + short_code

    return ShortenResponse(
        short_url=short_url,
        short_code=short_code,
        expires_at=request_data.expires_at,
    )


@app.get("/stats/{short_code}", response_model=URLStatsResponse)
def get_url_stats(
    short_code: str,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    stats = url_service.get_url_stats(short_code)

    if stats is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    return stats

@app.patch("/{short_code}", status_code=204)
def update_short_url(
    short_code: str,
    request_data: UpdateURLRequest,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    try:
        url_service.update_original_url(short_code, str(request_data.url))
    except ShortCodeNotFoundError:
        raise HTTPException(status_code=404, detail="Short code not found")

@app.get("/urls", response_model=URLListResponse)
def list_urls(
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    base_url = str(request.base_url)

    return url_service.list_urls(
        base_url=base_url,
        limit=limit,
        offset=offset,
    )

@app.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    try:
        original_url = url_service.get_original_url(short_code)
    except ExpiredShortCodeError:
        raise HTTPException(
            status_code=410,
            detail="Short URL has expired",
        )

    if original_url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    return RedirectResponse(original_url)

@app.delete("/{short_code}", status_code=204)
def delete_short_url(
    short_code: str,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    try:
        url_service.delete_short_url(short_code)
    except ShortCodeNotFoundError:
        raise HTTPException(status_code=404, detail="Short code not found")
    
