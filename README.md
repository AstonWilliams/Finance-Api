﻿# Stock News & Finance Data API

## Overview
This API continuously scrapes and stores news articles from PR Newswire and Business Wire, as well as financial data from Yahoo Finance. The data is stored in a SQLite database and can be accessed via various endpoints. Prometheus metrics are integrated for monitoring API performance.

## Table of Contents
1. [Purpose](#purpose)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Database Models](#database-models)
8. [Background Tasks](#background-tasks)
9. [Prometheus Metrics](#prometheus-metrics)
10. [Health Check](#health-check)
11. [Contributing](#contributing)
12. [License](#license)
13. [Author](#author)

## Purpose
The purpose of this API is to provide a continuous stream of financial news and stock data by scraping reputable sources like PR Newswire, Business Wire, and Yahoo Finance. This helps investors, financial analysts, and developers who need up-to-date news and financial data for making informed decisions or integrating into their applications.

## Features
- **Continuous Scraping**: Fetches news from PR Newswire and Business Wire every 10 minutes.
- **Financial Data**: Fetches financial data from Yahoo Finance every 20 seconds.
- **Database Storage**: Stores scraped data in a SQLite database.
- **API Endpoints**: Provides endpoints to access news articles and financial data.
- **Prometheus Metrics**: Integrates Prometheus metrics for monitoring.
- **Health Check**: Provides a health check endpoint.

## Requirements
- Python 3.8+
- FastAPI
- SQLAlchemy
- Requests
- LXML
- Prometheus-client
- Psutil
- Uvicorn

## Installation
1. **Clone the repository**:
    ```sh
    git clone https://github.com/AstonWilliams/Finance-Api.git
    cd stock-news-api
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv .venv
    source .venv/bin/activate   # For Windows: .\.venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the API**:
    ```sh
    uvicorn app.main:app --reload
    ```

## Usage
After starting the API, you can access it at `http://127.0.0.1:8000`.

## API Endpoints
### News Endpoints
- **Get Latest News**: Returns the latest news articles.
    ```http
    GET /news
    ```

### Yahoo Finance Data Endpoints
- **Get Financial Data**: Returns financial data from Yahoo Finance.
    ```http
    GET /yahoofinance
    ```

## Database Models
### NewsArticle
- `id`: Integer, primary key
- `title`: String, index
- `source`: String, index
- `published_date`: DateTime
- `content`: Text
- `hash`: String, unique, index

### YahooFinanceData
- `id`: Integer, primary key
- `symbol`: String, index
- `name`: String, index
- `change`: String
- `change_percent`: String
- `price_intraday`: String
- `ytd_return`: String
- `three_mo_return`: String
- `one_year`: String
- `three_year_return`: String
- `five_year_return`: String
- `net_expense_ratio`: String
- `gross_expense_ratio`: String
- `net_assets`: String
- `fifty_day_avg`: String
- `two_hundred_day_avg`: String
- `hash`: String, unique, index
- `timestamp`: DateTime

## Background Tasks
The API uses background tasks to continuously fetch data.
- **continuous_fetch**: Fetches news from PR Newswire and Business Wire every 10 minutes.
- **continuous_yahoo_finance_fetch**: Fetches financial data from Yahoo Finance every 20 seconds.

## Prometheus Metrics
Prometheus metrics are exposed at `/metrics` and `/metrics_json`.
- `request_count_total`: Total number of requests.
- `request_latency_seconds`: Request latency in seconds.
- `error_count_total`: Total number of errors.

## Health Check
A health check endpoint is available at `/health`. It provides the following metrics:
- `status`: Health status (`healthy` or `unhealthy`).
- `request_count`: Total number of requests.
- `error_count`: Total number of errors.
- `error_rate`: Error rate.
- `average_latency_seconds`: Average request latency.
- `cpu_usage_percent`: CPU usage percentage.
- `memory_usage_percent`: Memory usage percentage.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Author
- Name: A91060705
- Email: [a91060705@gmail.com](mailto:a91060705@gmail.com)
