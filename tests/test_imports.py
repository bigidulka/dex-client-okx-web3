import inspect
from dex_client_okx_web3 import OKXWeb3Client


def test_client_imports_and_instantiates():
    client = OKXWeb3Client()
    assert client is not None


def test_public_methods_present():
    methods = [name for name, value in inspect.getmembers(OKXWeb3Client, inspect.isfunction) if not name.startswith('_')]
    assert set(['ranking_content', 'ranking_config', 'token_overview', 'latest_info', 'risk_check', 'chain_list', 'config_info', 'tag_meta', 'tag_display_position', 'trading_history_filter_config', 'kline_bs_point_config', 'market_show_config', 'market_order_placer_strategy', 'tx_history_tag_filter', 'kline_bs_point', 'token_hlc_candles', 'trading_history', 'batch_token_basic_info', 'address_collect_support_chain', 'address_collect_simplify_query', 'search_token_support_chains', 'search_market_tag_meta', 'search_multi_source_hot', 'search_config', 'search_hot', 'search_correction', 'search_dapp_defi_top_list', 'search_unified', 'alert_web_get_app_key', 'list_alert_rules', 'alert_push_bind']) <= set(methods)
