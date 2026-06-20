from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse

from schemas import ShortenRequest, ShortenResponse, URLStatsResponse
from sqlite_storage import SQLiteURLRepository
from services import (
    URLShortenerService,
    InvalidShortCodeError,
    ShortCodeAlreadyExistsError,
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
        )
    except InvalidShortCodeError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except ShortCodeAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))

    short_url = str(request.base_url) + short_code

    return ShortenResponse(
        short_url=short_url,
        short_code=short_code,
    )


@app.get("/stats/{short_code}", response_model=URLStatsResponse)
def get_url_stats(
    short_code: str,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    stats = url_service.get_stats(short_code)

    if stats is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return stats


@app.get("/{short_code}")
def redirect_to_url(
    short_code: str,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    original_url = url_service.get_original_url(short_code)

    if original_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    url_service.record_click(short_code)

    return RedirectResponse(url=original_url)