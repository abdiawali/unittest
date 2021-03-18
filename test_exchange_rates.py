import unittest
from unittest import TestCase
from unittest.mock import patch

import bitcoin

class Test_bitcoin_rates(TestCase):

    @patch('bitcoin.api_call')
    def test_convert_dollars(self, mock_bitcoin_api):

        mock_bitcoin_api.return_value = {"time":{"updated":"Nov 19, 2020 22:00:00 UTC",
            "updatedISO":"2020-11-19T22:00:00+00:00",
            "updateduk":"Nov 19, 2020 at 22:00 GMT"},
            "disclaimer":"This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org","chartName":"Bitcoin",
            "bpi":{"USD":{"code":"USD","symbol":"&#36;","rate":"17,962.7805","description":"United States Dollar","rate_float":17962.7805},
            "GBP":{"code":"GBP","symbol":"&pound;","rate":"13,532.0990","description":"British Pound Sterling","rate_float":13532.099},
            "EUR":{"code":"EUR","symbol":"&euro;","rate":"15,121.6075","description":"Euro","rate_float":15121.6075}}}


        expected_dollars = 1796278.05
        dollars = bitcoin.get_bitcoin_value(100, 17962.7805)
        self.assertEqual(expected_dollars, dollars)

    @patch('bitcoin.api_call')
    def test_if_correct_rate_is_returned(self, mock_bitcoin_api):

        data = mock_bitcoin_api.return_value = {"time":{"updated":"Nov 19, 2020 22:00:00 UTC",
            "updatedISO":"2020-11-19T22:00:00+00:00",
            "updateduk":"Nov 19, 2020 at 22:00 GMT"},
            "disclaimer":"This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org","chartName":"Bitcoin",
            "bpi":{"USD":{"code":"USD","symbol":"&#36;","rate":"17,962.7805","description":"United States Dollar","rate_float":17962.7805},
            "GBP":{"code":"GBP","symbol":"&pound;","rate":"13,532.0990","description":"British Pound Sterling","rate_float":13532.099},
            "EUR":{"code":"EUR","symbol":"&euro;","rate":"15,121.6075","description":"Euro","rate_float":15121.6075}}}


        expected_rate = 17962.7805
        usd = bitcoin.extract_dollar_rate(data)
        self.assertEqual(expected_rate, usd)


    @patch('bitcoin.api_call')
    def test_api_call(self, mock_bitcoin_api):

        data = mock_bitcoin_api.return_value = {"time":{"updated":"Nov 19, 2020 22:00:00 UTC",
            "updatedISO":"2020-11-19T22:00:00+00:00",
            "updateduk":"Nov 19, 2020 at 22:00 GMT"},
            "disclaimer":"This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org","chartName":"Bitcoin",
            "bpi":{"USD":{"code":"USD","symbol":"&#36;","rate":"17,962.7805","description":"United States Dollar","rate_float":17962.7805},
            "GBP":{"code":"GBP","symbol":"&pound;","rate":"13,532.0990","description":"British Pound Sterling","rate_float":13532.099},
            "EUR":{"code":"EUR","symbol":"&euro;","rate":"15,121.6075","description":"Euro","rate_float":15121.6075}}}


        returned_data = bitcoin.api_call()
        self.assertEqual(data, returned_data)

    @patch('bitcoin.print')
    def test_display(self, mock_print):
        bitcoins = 100
        value = 5863437.630000001

        expected_print = '100.0 Bitcoin is worth $5863437.630000001'

        returned=bitcoin.display_exchange_rate(bitcoins, value)
        mock_print.asser_has_calls(expected_print)

    @patch('builtins.input', side_effect=['-1', '-100','-0.5', '0.5'])
    def test_non_positive_input(self, mock_input):
        bitcoins = bitcoin.get_bitcoin()
        self.assertEqual(0.5, bitcoins)


    @patch('builtins.input', side_effect=['hello', '123bitcoin','@$%^', '1'])
    def test_string_and_symbols(self, mock_input):
        bitcoins = bitcoin.get_bitcoin()
        self.assertEqual(1, bitcoins)


if __name__ == '__main__':
    unittest.main()