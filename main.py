from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse

from schemas import ShortenRequest, ShortenResponse
from storage import InMemoryURLRepository
from services import URLShortenerService


app = FastAPI()


repository = InMemoryURLRepository()
service = URLShortenerService(repository)


def get_url_shortener_service() -> URLShortenerService:
    return service


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(
    request_data: ShortenRequest,
    request: Request,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    short_code = url_service.create_short_url(str(request_data.url))

    short_url = f"{request.base_url}{short_code}"

    return ShortenResponse(
        short_code=short_code,
        short_url=short_url,
    )


@app.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    url_service: URLShortenerService = Depends(get_url_shortener_service),
):
    original_url = url_service.get_original_url(short_code)

    if original_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=original_url)