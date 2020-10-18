from tdsystem.crawler import TdsystemCrawler


def test_get_meet_result_buttons_2019():
    with TdsystemCrawler() as crawler:
        buttons = crawler._get_meet_result_buttons("2019")
        assert len(buttons) == 224
