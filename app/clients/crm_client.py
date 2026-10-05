import asyncio
import httpx
from app.config import settings


class CRMError(Exception):
    pass


class CRMClient:
    def __init__(self):
        self.base_url = settings.crm_base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {settings.crm_api_key}"}

    async def _request(self, method: str, path: str, **kwargs):
        last_error = None

        for attempt in range(settings.max_retries + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=settings.request_timeout,
                    headers=self.headers,
                ) as client:
                    response = await client.request(
                        method, f"{self.base_url}{path}", **kwargs
                    )

                if response.status_code == 429 or response.status_code >= 500:
                    if attempt < settings.max_retries:
                        retry_after = response.headers.get("Retry-After")
                        delay = float(retry_after) if retry_after else 2 ** attempt
                        await asyncio.sleep(delay)
                        continue

                if response.status_code >= 400:
                    raise CRMError(
                        f"CRM returned {response.status_code}: {response.text}"
                    )

                return response

            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt < settings.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue

        raise CRMError(f"CRM request failed after retries: {last_error}")

    async def list_customers(self, page: int = 1, page_size: int = 50):
        response = await self._request(
            "GET",
            "/customers",
            params={"page": page, "page_size": page_size},
        )
        return response.json()

    async def get_customer(self, external_id: str):
        response = await self._request("GET", f"/customers/{external_id}")
        return response.json()
