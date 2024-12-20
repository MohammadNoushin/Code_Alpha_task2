import yfinance as yf
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL
    )''')
    conn.commit()
    conn.close()

# Function to get the current stock price using yfinance
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        if not stock_info.empty:
            return stock_info['Close'][0]
        else:
            print(f"Could not fetch data for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Add a stock to the portfolio
def add_stock(symbol, shares):
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO portfolio (symbol, shares) VALUES (?, ?)', (symbol, shares))
        conn.commit()
        print(f"Added {shares} shares of {symbol} to the portfolio.")
    except Exception as e:
        print(f"Error adding stock: {e}")
    finally:
        conn.close()

# Remove a stock from the portfolio
def remove_stock(stock_id):
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    try:
        c.execute('DELETE FROM portfolio WHERE id = ?', (stock_id,))
        conn.commit()
        print(f"Removed stock with ID {stock_id} from the portfolio.")
    except Exception as e:
        print(f"Error removing stock: {e}")
    finally:
        conn.close()

# View the portfolio and its total value
def view_portfolio():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('SELECT * FROM portfolio')
    portfolio = c.fetchall()
    conn.close()

    if not portfolio:
        print("Your portfolio is empty.")
        return

    total_value = 0
    print("\nYour Portfolio:")
    for stock in portfolio:
        symbol = stock[1]
        shares = stock[2]
        price = get_stock_price(symbol)
        if price is not None:
            value = price * shares
            total_value += value
            print(f"{symbol}: {shares} shares @ ${price:.2f} = ${value:.2f}")
        else:
            print(f"{symbol}: Unable to fetch price")

    print(f"\nTotal Portfolio Value: ${total_value:.2f}")

# Main menu to interact with the user
def main():
    init_db()
    
    while True:
        print("\nStock Portfolio Tracker")
        print("1. View Portfolio")
        print("2. Add Stock")
        print("3. Remove Stock")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_portfolio()
        elif choice == '2':
            symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
            shares = input("Enter the number of shares: ")
            if shares.isdigit() and int(shares) > 0:
                add_stock(symbol, int(shares))
            else:
                print("Invalid number of shares. Please enter a positive integer.")
        elif choice == '3':
            try:
                stock_id = int(input("Enter the stock ID to remove: "))
                remove_stock(stock_id)
            except ValueError:
                print("Invalid stock ID. Please enter a valid integer.")
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == '__main__':
    main()