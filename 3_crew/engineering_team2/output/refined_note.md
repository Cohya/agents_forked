```markdown
# Key Objectives
- Develop a simple account management system for a trading simulation platform.
- Enable user account creation, fund deposits, and fund withdrawals.
- Allow users to record purchasing and selling shares, specifying the quantity.
- Calculate the user’s portfolio total value and identify profit or loss based on initial deposit.
- Provide real-time reporting of user holdings and profit/loss status.
- Maintain a transaction history accessible to users.
- Implement restrictions to prevent:
  - Withdrawals leading to negative account balance.
  - Purchases exceeding available funds.
  - Sales of shares not owned by the user.

# Constraints
- The system must ensure that user transactions comply with the defined restrictions.
- The system relies on the `get_share_price(symbol)` function for obtaining share prices.
- The share price function includes a test implementation with fixed prices for specific stocks (AAPL, TSLA, GOOGL).

# Open Questions
- What specific user interface requirements exist for the account management and reporting features?
- Are there any security measures that need to be implemented to protect user accounts and transactions?
- How should the system handle errors or exceptions during transactions (e.g., insufficient funds, invalid share quantities)?

# Assumptions
- Users of the trading simulation platform are familiar with basic trading concepts.
- The system will utilize the fixed price implementation of the `get_share_price(symbol)` function for testing purposes.
- Users expect real-time updates on their account balances, holdings, and transaction history.

# Additional Notes
- Incorporate a green color in the background of the user interface for a visually appealing design.
```