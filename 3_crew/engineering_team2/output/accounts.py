class Account:
    def __init__(self, username: str, initial_deposit: float):
        self.username = username
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.transactions.append({
            'type': 'deposit',
            'amount': initial_deposit,
            'balance': self.balance
        })

    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self.balance += amount
            self.transactions.append({
                'type': 'deposit',
                'amount': amount,
                'balance': self.balance
            })
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append({
                'type': 'withdraw',
                'amount': amount,
                'balance': self.balance
            })
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price = get_share_price(symbol)
        cost = price * quantity
        if cost <= self.balance:
            self.balance -= cost
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self.transactions.append({
                'type': 'buy',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'balance': self.balance
            })
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            price = get_share_price(symbol)
            revenue = price * quantity
            self.balance += revenue
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append({
                'type': 'sell',
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'balance': self.balance
            })
            return True
        return False

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        initial_deposit = self.transactions[0]['amount']
        current_value = self.get_portfolio_value()
        return current_value - initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transaction_history(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    prices = {'AAPL': 150.0, 'TSLA': 700.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 0.0)

# Testing the implementation creation
account = Account("john_doe", 10000.0)
print(account.deposit(500))
print(account.withdraw(200))
print(account.buy_shares('AAPL', 10))
print(account.sell_shares('AAPL', 5))
print(account.get_portfolio_value())
print(account.get_profit_loss())
print(account.get_holdings())
print(account.get_transaction_history())