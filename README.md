# Trade Tracker Web App

Trade Tracker is a web app that allows users to get stock quotes, journal trades, and analyze their trading performance. The app is built in Django and uses the Iexcloud API as an external source for stock quotes.

## Features

- Enter a ticker and get quotes from 3rd party API using GET and POST requests.
- Save trades, including ticker, # of shares, price, open and close date using POST requests.
- Delete trade info using DELETE requests.
- Edit trade info (shares, price, etc.) using PUT requests.
- Track trading performance using GET requests (future feature).
- Show charts and technical analysis indicators (future feature).
- Generate buy/sell signals (future feature).
- Calculate position size based on Kelly Criterion and perform Monte Carlo simulations of Kelly formula (future feature).

## Database Schema

The app uses a PostgreSQL database with the following schema:

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

### Users table (future feature)

| Column   | Data Type | Description              |
| -------- | --------- | ------------------------ |
| username | varchar   | User's username          |
| password | varchar   | User's password (hashed) |
| capital  | float     | User's available capital |

## Project Installation

Follow these steps to install and set up the project:

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/your-project.git
   cd your-project
   ```

2. Set up a virtual environment (optional but recommended):

   ```shell
   python -m venv env
   source env/bin/activate   # For Linux/Mac
   env\Scripts\activate     # For Windows
   ```

3. Install the project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:

   - Make sure you have PostgreSQL installed and running on your system.
   - Create a new PostgreSQL database for your project.
   - Update the database configuration in the `settings.py` file with the appropriate credentials and connection details for your PostgreSQL database.

5. Apply database migrations:

   ```shell
   python manage.py migrate
   ```

6. (Optional) Create a superuser account:

   ```shell
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```shell
   python manage.py runserver
   ```

The application should now be running locally on `http://localhost:8000`. Access it in your web browser to start using the project.

**Note:** If you're deploying the project to a production environment, make sure to follow the appropriate steps for setting up and configuring a PostgreSQL database in your production environment.

## Usage

To use the app, follow these steps:

1. Enter a ticker symbol to get quotes from the 3rd party API.
2. Add or delete quotes from the watchlist.
3. Journal trades by entering the ticker, # of shares, price, open and close date.
4. Delete or edit trade information as needed.
5. Track your portfolio performance by retrieving your trades.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions to this project are welcome. If you find any bugs or want to suggest new features, please open an issue or submit a pull request.

Thank you for using Trade Tracker!