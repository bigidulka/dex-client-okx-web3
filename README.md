        # OKX Web3 Reverse Client

        Python client for endpoints used by [https://web3.okx.com](https://web3.okx.com). The implementation is browser/reverse-engineered and mirrors the internal clients used in local DEX modules.

        ## Install

        ```bash
        pip install git+https://github.com/bigidulka/dex-client-okx-web3.git
        ```

        For local development:

        ```bash
        pip install -e '.[dev]'
        pytest
        ```

        ## Quick start

        ```python
        from dex_client_okx_web3 import OKXWeb3Client

        client = OKXWeb3Client()
        # call any method below; all methods return decoded JSON dict/list payloads
        ```

        ## Methods

        - `ranking_content`
- `ranking_config`
- `token_overview`
- `latest_info`
- `risk_check`
- `chain_list`
- `config_info`
- `tag_meta`
- `tag_display_position`
- `trading_history_filter_config`
- `kline_bs_point_config`
- `market_show_config`
- `market_order_placer_strategy`
- `tx_history_tag_filter`
- `kline_bs_point`
- `token_hlc_candles`
- `trading_history`
- `batch_token_basic_info`
- `address_collect_support_chain`
- `address_collect_simplify_query`
- `search_token_support_chains`
- `search_market_tag_meta`
- `search_multi_source_hot`
- `search_config`
- `search_hot`
- `search_correction`
- `search_dapp_defi_top_list`
- `search_unified`
- `alert_web_get_app_key`
- `list_alert_rules`
- `alert_push_bind`

        ## Endpoint inventory

        Extracted from existing Local clients and rechecked with browser-harness network capture where the site allowed capture.

        - `['GET', '/priapi/v1/dx/market/v3/advanced/ranking/content', 'advanced ranking content']`
- `['GET', '/priapi/v1/dx/market/v3/advanced/ranking/config', 'advanced ranking config']`
- `['GET', '/priapi/v1/dx/market/v2/token/overview', 'token overview']`
- `['GET', '/priapi/v1/dx/market/v2/latest/info', 'latest info']`
- `['GET', '/priapi/v1/dx/market/v2/risk/new/check', 'risk check']`
- `['GET', '/priapi/v1/dx/market/v2/chain/list', 'chain list']`
- `['GET', '/priapi/v1/dx/market/v2/config/info', 'config info']`
- `['GET', '/priapi/v1/dx/market/tag/meta', 'tag meta']`
- `['GET', '/priapi/v1/dx/market/tag/displayPosition', 'tag display position']`
- `['GET', '/priapi/v1/dx/market/tag/txHistoryTagFilter', 'tx history tag filter']`
- `['POST', '/priapi/v1/dx/market/v2/trading-history/filter-list', 'trading history']`
- `['GET', '/priapi/v1/dx/market/v2/trading-history/filter-config', 'history filter config']`
- `['GET', '/priapi/v1/dx/market/v2/trading/kline-bs-point', 'kline buy/sell points']`
- `['GET', '/priapi/v1/dx/market/v2/trading/kline-bs-point/config', 'kline buy/sell config']`
- `['GET', '/priapi/v1/dx/trade/multi/marketShowConfig', 'market show config']`
- `['GET', '/priapi/v1/dx/trade/multi/marketOrderPlacerStrategy', 'market order placer strategy']`
- `['POST', '/priapi/v1/dx/market/v2/batch/token/basic/info', 'batch token basic info']`
- `['GET', '/priapi/v5/dex/token/market/dex-token-hlc-candles', 'dex token HLC candles']`
- `['GET', '/priapi/v1/dx/market/v2/address/collect/support/chain', 'address collect support chain']`
- `['GET', '/priapi/v1/dx/market/v2/address/collect/simplify/query', 'address collect simplify query']`
- `['GET', '/priapi/v2/wallet/search/market/token-support-chains', 'search token support chains']`
- `['GET', '/priapi/v2/wallet/search/market/tag/meta', 'search market tag meta']`
- `['GET', '/priapi/v2/wallet/search/multi-source-hot', 'multi source hot search']`
- `['GET', '/priapi/v2/wallet/search/config', 'search config']`
- `['GET', '/priapi/v2/wallet/search/hot', 'search hot']`
- `['GET', '/priapi/v2/wallet/search/correction', 'search correction']`
- `['GET', '/priapi/v2/wallet/search/dapp/defi-top-list', 'dapp defi top list']`
- `['POST', '/priapi/v2/wallet/search/unified', 'unified search']`
- `['GET', '/priapi/v1/dx/market/v2/alert/web/get-app-key', 'alert app key']`
- `['POST', '/priapi/v1/dx/market/v2/listAlertRules', 'alert rules']`
- `['POST', '/priapi/v1/dx/market/v2/alert/web/push-bind', 'alert push bind']`

        Full details: [`endpoint_inventory.json`](endpoint_inventory.json).

        ## Notes

        - No official SDK is used.
        - Some endpoints require Cloudflare/browser behavior; pass `use_curl_cffi=True` where available.
        - Auth/session-only methods need your own cookies/tokens. Do not commit secrets.
        - These clients are thin transport wrappers; normalize data in your application layer.
