
# GNews MCP Server

## Overview
This project demonstrates how to expose external REST APIs as AI-callable tools using the Model Context Protocol (MCP) and FastMCP in Python.

## Features
- Get top headlines
- Search news by keyword
- Get news by topic
- Get news by date range
- Input validation and error handling
- Async API calls using httpx

## Project Structure

GNews_MCP/
│
├── app/
│   ├── __init__.py
│   └── server.py
│
├── screenshots/
├── README.md
├── requirements.txt
├── .env
└── .gitignore

## Setup Instructions

### 1. Create Virtual Environment

Windows:
python -m venv .venv

Activate:
.venv\Scripts\activate

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Add API Key

Create a .env file:

GNEWS_API_KEY=your_api_key_here

### 4. Run MCP Inspector

npx @modelcontextprotocol/inspector python app/server.py

Open:
http://localhost:6274

## Tools Implemented

1. get_top_headlines
2. search_news
3. get_news_by_topic
4. get_news_by_date_range

## Error Handling
- Invalid country codes
- Invalid topics
- Empty queries
- Long queries
- Invalid date formats
- Invalid date ranges
- API/network failures

## Technologies Used
- Python
- FastMCP
- MCP
- httpx
- python-dotenv
- GNews API
