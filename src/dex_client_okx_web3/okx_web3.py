from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid
from typing import Any

from .core import BaseClient, DEFAULT_UA, Json, now_ms


def generate_okx_site_info(region: str = "BY", code: str = "OKX_GLOBAL", entity: int = 18) -> str:
    raw = json.dumps({"region": region, "code": code, "entity": entity}, separators=(",", ":"))
    return "=" + base64.b64encode(raw.encode()).decode()[::-1]


def generate_okx_auth(url_path: str, method: str, body: str = "", token: str | None = None, timestamp_ms: int | None = None) -> tuple[str, int, str]:
    token = token or str(uuid.uuid4())
    timestamp = timestamp_ms or now_ms()
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    seconds = timestamp // 1000
    f = (seconds // 600) % 32
    d = (seconds // 3600) % 32
    key = "".join(token_hash[(f + (d + p) * p) % 32] for p in range(32)).encode()
    message = url_path.replace("?", "")
    if method.upper() in {"POST", "PUT"} and body:
        message = url_path.split("?", 1)[0] + body
    signature = base64.b64encode(hmac.new(key, message.encode(), hashlib.sha256).digest()).decode()
    return token, timestamp, signature


class OKXWeb3Client(BaseClient):
    def __init__(self, *, base_url: str = "https://web3.okx.com", timeout: float = 10.0, use_curl_cffi: bool = False):
        super().__init__(base_url, timeout=timeout, use_curl_cffi=use_curl_cffi)
        self.device_id = str(uuid.uuid4())

    def _headers(self, url_path: str, method: str, body: str = "", *, site_info: bool = False) -> dict[str, str]:
        token, ts, sign = generate_okx_auth(url_path, method, body)
        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "app-type": "web",
            "platform": "web",
            "devid": self.device_id,
            "device-token": self.device_id,
            "ok-verify-token": token,
            "ok-timestamp": str(ts),
            "ok-verify-sign": sign,
            "x-locale": "en_US",
            "x-utc": "3",
            "x-cdn": "https://web3.okx.com",
            "x-zkdex-env": "0",
            "origin": "https://web3.okx.com",
            "referer": "https://web3.okx.com/",
            "user-agent": DEFAULT_UA,
        }
        if method.upper() in {"POST", "PUT"}:
            headers["content-type"] = "application/json"
        if site_info:
            headers["x-site-info"] = generate_okx_site_info()
        return headers

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Json:
        params = {**(params or {}), "t": now_ms()}
        from urllib.parse import urlencode
        url_path = path + "?" + urlencode(params)
        return self.get(path, params=params, headers=self._headers(url_path, "GET"))

    def _post(self, path: str, body: Any, *, curl_cffi: bool = False) -> Json:
        body_text = json.dumps(body, separators=(",", ":"))
        params = {"t": now_ms()}
        url_path = f"{path}?t={params['t']}"
        return self.post(path, params=params, json_body=body, headers=self._headers(url_path, "POST", body_text, site_info=True), curl_cffi=curl_cffi)

    def ranking_content(self, chain_id: str = "1", page: int = 1, page_size: int = 200, category_type: int = 4, min_liquidity: int = 1000) -> Json:
        return self._get("/priapi/v1/dx/market/v3/advanced/ranking/content", {"chainId": chain_id, "categoryType": category_type, "pageSize": page_size, "page": page, "liquidityMin": min_liquidity})

    def ranking_config(self, platform_type: int = 2) -> Json:
        return self._get("/priapi/v1/dx/market/v3/advanced/ranking/config", {"platformType": platform_type})

    def token_overview(self, chain_id: str, token_contract_address: str) -> Json:
        return self._get("/priapi/v1/dx/market/v2/token/overview", {"chainId": chain_id, "tokenContractAddress": token_contract_address})

    def latest_info(self, chain_id: str, token_contract_address: str) -> Json:
        return self._get("/priapi/v1/dx/market/v2/latest/info", {"chainId": chain_id, "tokenContractAddress": token_contract_address})

    def risk_check(self, chain_id: str, token_contract_address: str) -> Json:
        return self._get("/priapi/v1/dx/market/v2/risk/new/check", {"chainId": chain_id, "tokenContractAddress": token_contract_address})

    def chain_list(self) -> Json: return self._get("/priapi/v1/dx/market/v2/chain/list")
    def config_info(self) -> Json: return self._get("/priapi/v1/dx/market/v2/config/info")
    def tag_meta(self) -> Json: return self._get("/priapi/v1/dx/market/tag/meta")
    def tag_display_position(self) -> Json: return self._get("/priapi/v1/dx/market/tag/displayPosition")
    def trading_history_filter_config(self) -> Json: return self._get("/priapi/v1/dx/market/v2/trading-history/filter-config")
    def kline_bs_point_config(self) -> Json: return self._get("/priapi/v1/dx/market/v2/trading/kline-bs-point/config")
    def market_show_config(self) -> Json: return self._get("/priapi/v1/dx/trade/multi/marketShowConfig")
    def market_order_placer_strategy(self) -> Json: return self._get("/priapi/v1/dx/trade/multi/marketOrderPlacerStrategy")

    def tx_history_tag_filter(self, chain_id: str, token_contract_address: str) -> Json:
        return self._get("/priapi/v1/dx/market/tag/txHistoryTagFilter", {"chainId": chain_id, "tokenContractAddress": token_contract_address})

    def kline_bs_point(self, chain_id: str, token_address: str, *, bar: str = "1s", from_address_tags: str = "migrate-for-bs,dev,kol-for-bs") -> Json:
        return self._get("/priapi/v1/dx/market/v2/trading/kline-bs-point", {"chainId": chain_id, "tokenAddress": token_address, "fromAddressTags": from_address_tags, "bar": bar})

    def token_hlc_candles(self, chain_id: str, address: str, *, bar: str = "1m", limit: int = 300, before: int | None = None, after: int | None = None) -> Json:
        params: dict[str, Any] = {"chainId": chain_id, "address": address, "bar": bar, "limit": limit}
        if before: params["before"] = before
        if after: params["after"] = after
        return self._get("/priapi/v5/dex/token/market/dex-token-hlc-candles", params)

    def trading_history(self, chain_id: str, token_contract_address: str, *, type: str = "0", limit: int = 30, desc: bool = True, order_by: str = "timestamp", user_address_list: list[str] | None = None, volume_min: str = "", volume_max: str = "", price_min: str = "", price_max: str = "", amount_min: str = "", amount_max: str = "") -> Json:
        body = {"desc": desc, "orderBy": order_by, "limit": limit, "tradingHistoryFilter": {"chainId": str(chain_id), "tokenContractAddress": token_contract_address, "type": type, "currentUserWalletAddress": "", "userAddressList": user_address_list or [], "volumeMin": volume_min, "volumeMax": volume_max, "priceMin": price_min, "priceMax": price_max, "amountMin": amount_min, "amountMax": amount_max}}
        return self._post("/priapi/v1/dx/market/v2/trading-history/filter-list", body, curl_cffi=True)

    def batch_token_basic_info(self, tokens: list[tuple[str | int, str]]) -> Json:
        body = [{"chainId": int(chain), "tokenAddress": token} for chain, token in tokens]
        return self._post("/priapi/v1/dx/market/v2/batch/token/basic/info", body)

    def address_collect_support_chain(self) -> Json: return self._get("/priapi/v1/dx/market/v2/address/collect/support/chain")
    def address_collect_simplify_query(self, wallet_address: str) -> Json: return self._get("/priapi/v1/dx/market/v2/address/collect/simplify/query", {"walletAddress": wallet_address})
    def search_token_support_chains(self) -> Json: return self._get("/priapi/v2/wallet/search/market/token-support-chains")
    def search_market_tag_meta(self) -> Json: return self._get("/priapi/v2/wallet/search/market/tag/meta")
    def search_multi_source_hot(self) -> Json: return self._get("/priapi/v2/wallet/search/multi-source-hot")
    def search_config(self) -> Json: return self._get("/priapi/v2/wallet/search/config")
    def search_hot(self) -> Json: return self._get("/priapi/v2/wallet/search/hot")
    def search_correction(self, query: str) -> Json: return self._get("/priapi/v2/wallet/search/correction", {"query": query})
    def search_dapp_defi_top_list(self) -> Json: return self._get("/priapi/v2/wallet/search/dapp/defi-top-list")

    def search_unified(self, keyword: str, *, page_num: int = 1, page_size: int = 15, sources: list[str] | None = None) -> Json:
        body = {"keyword": keyword, "periodType": 3, "discoverSearchParam": {"pageNum": page_num, "pageSize": page_size}, "tabChainFilter": {"token": None, "stock": None, "preciousMetal": None}, "sources": sources or ["token", "address", "discover", "kol"]}
        return self._post("/priapi/v2/wallet/search/unified", body)

    def alert_web_get_app_key(self, domain: str = "web3.okx.com") -> Json: return self._get("/priapi/v1/dx/market/v2/alert/web/get-app-key", {"domain": domain})
    def list_alert_rules(self, body: dict[str, Any] | None = None) -> Json: return self._post("/priapi/v1/dx/market/v2/listAlertRules", body or {})
    def alert_push_bind(self, body: dict[str, Any] | None = None) -> Json: return self._post("/priapi/v1/dx/market/v2/alert/web/push-bind", body or {})
