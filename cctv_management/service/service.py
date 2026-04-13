import os
from typing import Any

import requests
import xmltodict


class CctvManagementService:
    def __init__(self):
        self.api_key = os.getenv("TAGO_API_KEY")
        self.base_url = os.getenv("TAGO_BASE_URL", "https://openapi.its.go.kr:9443")
        self.cctv_endpoint = os.getenv("TAGO_CCTV_ENDPOINT", "/cctvInfo")
        self.default_type = os.getenv("TAGO_CCTV_QUERY_TYPE", "all")
        self.default_cctv_type = os.getenv("TAGO_CCTV_TYPE", "1")
        self.default_min_x = os.getenv("TAGO_CCTV_MIN_X", "126.8")
        self.default_max_x = os.getenv("TAGO_CCTV_MAX_X", "127.2")
        self.default_min_y = os.getenv("TAGO_CCTV_MIN_Y", "37.4")
        self.default_max_y = os.getenv("TAGO_CCTV_MAX_Y", "37.7")

    def list_cctvs(
        self,
        region: str | None = None,
        limit: int = 50,
        min_x: float | None = None,
        max_x: float | None = None,
        min_y: float | None = None,
        max_y: float | None = None,
    ) -> dict[str, Any]:
        payload = self._fetch_cctv_data(
            region=region,
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
        )
        if payload is None:
            return {"ok": False, "message": "CCTV 목록 조회 실패"}

        items = self._extract_items(payload)
        normalized = [self._normalize_item(item) for item in items]
        normalized = [item for item in normalized if item["cctv_id"] is not None]

        if region:
            key = region.lower()
            normalized = [
                item
                for item in normalized
                if key in (item.get("location") or "").lower()
                or key in (item.get("name") or "").lower()
            ]

        return {
            "ok": True,
            "source": "TAGO",
            "count": len(normalized[:limit]),
            "items": normalized[:limit],
        }

    def get_cctv_detail(self, cctv_id: int) -> dict[str, Any]:
        payload = self._fetch_cctv_data(cctv_id=cctv_id)
        if payload is None:
            return {"ok": False, "message": "CCTV 상세 조회 실패", "cctv_id": cctv_id}

        items = [self._normalize_item(item) for item in self._extract_items(payload)]
        target = next((item for item in items if item.get("cctv_id") == cctv_id), None)

        if target is None and items:
            target = items[0]

        if target is None:
            return {"ok": False, "message": "해당 CCTV를 찾을 수 없음", "cctv_id": cctv_id}

        return {"ok": True, "source": "TAGO", "item": target}

    def get_stream_url(self, cctv_id: int) -> dict[str, Any]:
        detail = self.get_cctv_detail(cctv_id)
        if not detail.get("ok"):
            return detail

        item = detail["item"]
        stream_url = item.get("stream_url")
        if not stream_url:
            return {
                "ok": False,
                "message": "스트리밍 URL이 없음",
                "cctv_id": cctv_id,
            }

        return {
            "ok": True,
            "source": "TAGO",
            "cctv_id": item.get("cctv_id", cctv_id),
            "stream_url": stream_url,
            "name": item.get("name"),
            "location": item.get("location"),
        }

    def _fetch_cctv_data(
        self,
        cctv_id: int | None = None,
        region: str | None = None,
        min_x: float | None = None,
        max_x: float | None = None,
        min_y: float | None = None,
        max_y: float | None = None,
    ) -> dict[str, Any] | None:
        if not self.api_key:
            return None

        url = f"{self.base_url.rstrip('/')}{self.cctv_endpoint}"
        params = {
            "apiKey": self.api_key,
            "getType": "json",
            "type": self.default_type,
            "cctvType": self.default_cctv_type,
            "minX": min_x if min_x is not None else self.default_min_x,
            "maxX": max_x if max_x is not None else self.default_max_x,
            "minY": min_y if min_y is not None else self.default_min_y,
            "maxY": max_y if max_y is not None else self.default_max_y,
        }
        if cctv_id is not None:
            params["cctvId"] = cctv_id
        if region:
            params["region"] = region

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except ValueError:
            try:
                return xmltodict.parse(response.text)
            except Exception:
                return None
        except requests.exceptions.RequestException:
            return None

    def _extract_items(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        if not isinstance(payload, dict):
            return []

        response = payload.get("response", payload)
        if isinstance(response, dict) and isinstance(response.get("data"), list):
            return [i for i in response.get("data", []) if isinstance(i, dict)]

        body = response.get("body", response) if isinstance(response, dict) else {}
        items = body.get("items", body) if isinstance(body, dict) else {}

        if isinstance(items, dict) and "item" in items:
            items = items["item"]

        if isinstance(items, list):
            return [i for i in items if isinstance(i, dict)]
        if isinstance(items, dict):
            return [items]
        return []

    def _normalize_item(self, item: dict[str, Any]) -> dict[str, Any]:
        cctv_id = self._to_int(
            item.get("cctvId") or item.get("id") or item.get("cctv_id")
        )
        if cctv_id is None:
            raw_id = f"{item.get('cctvname') or item.get('cctvName')}-{item.get('coordx')}-{item.get('coordy')}"
            cctv_id = abs(hash(raw_id)) % 1_000_000_000

        return {
            "cctv_id": cctv_id,
            "name": item.get("cctvName") or item.get("name") or item.get("cameraName"),
            "location": item.get("location") or item.get("address") or item.get("cctvLocation"),
            "stream_url": item.get("cctvurl") or item.get("streamUrl") or item.get("url"),
            "direction": item.get("direction") or item.get("direct") or item.get("cctvType"),
            "latitude": self._to_float(item.get("lat") or item.get("latitude") or item.get("coordy") or item.get("y")),
            "longitude": self._to_float(item.get("lon") or item.get("longitude") or item.get("coordx") or item.get("x")),
            "raw": item,
        }

    @staticmethod
    def _to_int(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_float(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None