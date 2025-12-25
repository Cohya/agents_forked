import unittest
from unittest.mock import patch
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('john_doe', 10000.0)

    def test_initial_deposit(self):
        self.assertEqual(self.account.balance, 10000.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'deposit')

    def test_deposit(self):
        result = self.account.deposit(500)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 10500.0)

    def test_withdraw_success(self):
        result = self.account.withdraw(500)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 9500.0)

    def test_withdraw_failure(self):
        result = self.account.withdraw(15000)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 10000.0)

    @patch('accounts.get_share_price', return_value=150.0)
    def test_buy_shares(self, mock_get_share_price):
        result = self.account.buy_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 8500.0)
        self.assertIn('AAPL', self.account.holdings)
        self.assertEqual(self.account.holdings['AAPL'], 10)

    @patch('accounts.get_share_price', return_value=150.0)
    def test_sell_shares(self, mock_get_share_price):
        self.account.holdings = {'AAPL': 10}
        result = self.account.sell_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 10750.0)
        self.assertIn('AAPL', self.account.holdings)
        self.assertEqual(self.account.holdings['AAPL'], 5)

    @patch('accounts.get_share_price', return_value=150.0)
    def test_get_portfolio_value(self, mock_get_share_price):
        self.account.holdings = {'AAPL': 10}
        portfolio_value = self.account.get_portfolio_value()
        self.assertEqual(portfolio_value, 11500.0)

    @patch('accounts.get_share_price', return_value=150.0)
    def test_get_profit_loss(self, mock_get_share_price):
        self.account.holdings = {'AAPL': 10}
        profit_loss = self.account.get_profit_loss()
        self.assertEqual(profit_loss, 1500.0)

    def test_get_holdings(self):
        self.account.holdings = {'AAPL': 10}
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 10})

    def test_get_transaction_history(self):
        self.account.deposit(500)
        self.account.withdraw(200)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 3)

if __name__ == '__main__':
    unittest.main()