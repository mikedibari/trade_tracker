# Trade Tracker Web App

Trade Tracker is a web app that allows users to get stock quotes, journal trades, and analyze their trading performance. The app is built in Django and uses the Iexcloud API as an external source for stock quotes.

## Features

- Enter a ticker and get quotes from 3rd party API using GET and POST requests.
- Save trades, including ticker, # of shares, price, open and close date using POST requests.
- Delete trade info using DELETE requests.
- Edit trade info (shares, price, etc.) using PUT requests.
- Track portfolio performance using GET requests.
- Show charts and technical analysis indicators (future feature).
- Generate buy/sell signals (future feature).
- Calculate position size based on Kelly Criterion and perform Monte Carlo simulations of Kelly formula (future feature).

## Database Schema

The app uses a SQLite database with the following schema:

### Stocks table

| Column    | Data Type | Description                            |
| --------- | --------- | -------------------------------------- |
| ticker    | varchar   | Stock symbol                           |
| buy_price | float     | Buy price per share                     |
| sell_price| float     | Sell price per share                    |
| shares    | integer   | Number of shares bought or sold        |
| open_date | datetime  | Date and time the position was opened  |
| close_date| datetime  | Date and time the position was closed  |

### Quotes table

| Column      | Data Type | Description           |
| ----------- | --------- | --------------------- |
| ticker      | varchar   | Stock symbol          |
| company_name| varchar   | Company name          |

### Users table

| Column   | Data Type | Description              |
| -------- | --------- | ------------------------ |
| username | varchar   | User's username          |
| password | varchar   | User's password (hashed) |
| capital  | float     | User's available capital |

## Installation

1. Clone the repository to your local machine.
2. Install Python 3.x.
3. Install the required packages using the command pip install -r requirements.txt.
4. Create a .env file in the root directory of the project and set the api_key environment variable using Python decouple: api_key=<your_iexcloud_api_key>
5. Run the server using python manage.py runserver
6. Access the app by navigating to `http://localhost:8000` in your web browser.

## Usage

To use the app, follow these steps:

1. Enter a ticker symbol to get quotes from the 3rd party API.
2. Journal trades by entering the ticker, # of shares, price, open and close date.
3. Delete or edit trade information as needed.
4. Track your portfolio performance by retrieving your trades.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions to this project are welcome. If you find any bugs or want to suggest new features, please open an issue or submit a pull request.

Thank you for using Trade Tracker!