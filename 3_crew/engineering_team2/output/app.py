import gradio as gr

class Account:
    def __init__(self):
        self.balance = 0.0
        self.holdings = {}
        self.transaction_history = []
        self.initial_deposit = 0.0

    def create_account(self, initial_deposit):
        self.initial_deposit = initial_deposit
        self.balance += initial_deposit
        return f"Account created with initial deposit of ${initial_deposit:.2f}"

    def deposit(self, amount):
        self.balance += amount
        return f"Deposited ${amount:.2f}. Current balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        if self.balance - amount < 0:
            return "Error: Insufficient funds for withdrawal."
        self.balance -= amount
        return f"Withdrew ${amount:.2f}. Current balance: ${self.balance:.2f}"

    def buy_shares(self, symbol, quantity):
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.balance:
            return "Error: Insufficient funds to buy shares."
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transaction_history.append(f"Bought {quantity} shares of {symbol} at ${price:.2f} each.")
        return f"Bought {quantity} shares of {symbol}. Current balance: ${self.balance:.2f}"

    def sell_shares(self, symbol, quantity):
        if self.holdings.get(symbol, 0) < quantity:
            return "Error: Insufficient shares to sell."
        price = get_share_price(symbol)
        total_revenue = price * quantity
        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transaction_history.append(f"Sold {quantity} shares of {symbol} at ${price:.2f} each.")
        return f"Sold {quantity} shares of {symbol}. Current balance: ${self.balance:.2f}"

    def get_portfolio_value(self):
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return f"Total portfolio value: ${total_value:.2f}"

    def get_profit_loss(self):
        total_value = self.get_portfolio_value()
        profit_loss = total_value - self.initial_deposit
        return f"Profit/Loss since initial deposit: ${profit_loss:.2f}"

    def get_holdings(self):
        return self.holdings

    def get_transactions(self):
        return self.transaction_history

def get_share_price(symbol):
    fixed_prices = {"AAPL": 150.0, "TSLA": 700.0, "GOOGL": 2800.0}
    return fixed_prices.get(symbol, 0)

account = Account()

def create_account(initial_deposit):
    return account.create_account(initial_deposit)

def deposit(amount):
    return account.deposit(amount)

def withdraw(amount):
    return account.withdraw(amount)

def buy_shares(symbol, quantity):
    return account.buy_shares(symbol, quantity)

def sell_shares(symbol, quantity):
    return account.sell_shares(symbol, quantity)

def portfolio_value():
    return account.get_portfolio_value()

def profit_loss():
    return account.get_profit_loss()

def holdings():
    return account.get_holdings()

def transactions():
    return account.get_transactions()

with gr.Blocks(theme=gr.themes.Default(primary_hue="green")) as demo:
    gr.Markdown("## Trading Simulation Platform")
    
    with gr.Row():
        with gr.Column():
            initial_deposit = gr.Number(label="Initial Deposit", value=1000)
            create_button = gr.Button("Create Account")
            create_output = gr.Textbox(label="Account Status")
        
            deposit_amount = gr.Number(label="Deposit Amount")
            deposit_button = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Deposit Status")
        
            withdraw_amount = gr.Number(label="Withdraw Amount")
            withdraw_button = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Withdraw Status")
        
            symbol = gr.Textbox(label="Stock Symbol (AAPL/TSLA/GOOGL)")
            buy_quantity = gr.Number(label="Buy Quantity")
            buy_button = gr.Button("Buy Shares")
            buy_output = gr.Textbox(label="Buy Status")
        
            sell_quantity = gr.Number(label="Sell Quantity")
            sell_button = gr.Button("Sell Shares")
            sell_output = gr.Textbox(label="Sell Status")

    with gr.Row():
        portfolio_button = gr.Button("Get Portfolio Value")
        portfolio_output = gr.Textbox(label="Portfolio Value")
        
        profit_loss_button = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss Status")
        
        holdings_button = gr.Button("Get Holdings")
        holdings_output = gr.Textbox(label="Current Holdings")
        
        transactions_button = gr.Button("Get Transactions")
        transactions_output = gr.Textbox(label="Transaction History")

    create_button.click(create_account, inputs=initial_deposit, outputs=create_output)
    deposit_button.click(deposit, inputs=deposit_amount, outputs=deposit_output)
    withdraw_button.click(withdraw, inputs=withdraw_amount, outputs=withdraw_output)
    buy_button.click(buy_shares, inputs=[symbol, buy_quantity], outputs=buy_output)
    sell_button.click(sell_shares, inputs=[symbol, sell_quantity], outputs=sell_output)
    portfolio_button.click(portfolio_value, outputs=portfolio_output)
    profit_loss_button.click(profit_loss, outputs=profit_loss_output)
    holdings_button.click(holdings, outputs=holdings_output)
    transactions_button.click(transactions, outputs=transactions_output)

demo.launch()