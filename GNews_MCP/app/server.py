import os
import logging
from datetime import datetime

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# ------------------------------------------------
# Logging Configuration
# ------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------
# Load Environment Variables
# ------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")

if not API_KEY:
    raise ValueError(
        "Missing GNEWS_API_KEY in .env file"
    )

BASE_URL = "https://gnews.io/api/v4"

# ------------------------------------------------
# Initialize MCP Server
# ------------------------------------------------
mcp = FastMCP("GNews MCP Server")


# ------------------------------------------------
# Reusable Helper Function
# ------------------------------------------------
async def fetch_news(endpoint: str, params: dict) -> str:
    """
    Reusable helper function to fetch news.
    """

    params["apikey"] = API_KEY

    try:

        async with httpx.AsyncClient(
            timeout=30
        ) as client:

            response = await client.get(
                f"{BASE_URL}/{endpoint}",
                params=params
            )

        if response.status_code != 200:

            return (
                f"API Error "
                f"({response.status_code}): "
                f"{response.text}"
            )

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            return "No articles found."

        formatted_articles = []

        for idx, article in enumerate(
            articles,
            start=1
        ):

            formatted_articles.append(
                f"""
Article {idx}
--------------------------------
Title: {article.get("title")}
Source: {article.get("source", {}).get("name")}
Published At: {article.get("publishedAt")}
URL: {article.get("url")}
Description: {article.get("description")}
"""
            )

        return "\n".join(formatted_articles)

    except httpx.RequestError as e:
        return f"Network Error: {str(e)}"

    except Exception as e:
        return f"Unexpected Error: {str(e)}"


# ------------------------------------------------
# Tool 1: Get Top Headlines
# ------------------------------------------------
@mcp.tool()
async def get_top_headlines(
    category: str = "general",
    country: str = "us",
    language: str = "en",
    max_results: int = 5
) -> str:
    """
    Fetch top headlines by category.
    """

    logger.info("Fetching top headlines")

    allowed_countries = [
        "us",
        "in",
        "gb",
        "au",
        "ca"
    ]

    if country not in allowed_countries:

        return (
            f"Invalid country code '{country}'. "
            f"Allowed: "
            f"{', '.join(allowed_countries)}"
        )

    params = {
        "category": category,
        "country": country,
        "lang": language,
        "max": max_results
    }

    return await fetch_news(
        "top-headlines",
        params
    )


# ------------------------------------------------
# Tool 2: Search News
# ------------------------------------------------
@mcp.tool()
async def search_news(
    query: str,
    language: str = "en",
    max_results: int = 5,
    sort_by: str = "publishedAt"
) -> str:
    """
    Search news using keywords.
    """

    query = query.strip()

    logger.info(f"Searching news for: {query}")

    if not query:
        return "Search query cannot be empty."

    if len(query) > 100:
        return (
            "Query too long. "
            "Maximum 100 characters allowed."
        )

    allowed_sort = [
        "publishedAt",
        "relevance"
    ]

    if sort_by not in allowed_sort:

        return (
            f"Invalid sort_by '{sort_by}'. "
            f"Allowed: "
            f"{', '.join(allowed_sort)}"
        )

    params = {
        "q": query,
        "lang": language,
        "max": max_results,
        "sortby": sort_by
    }

    return await fetch_news(
        "search",
        params
    )


# ------------------------------------------------
# Tool 3: Get News By Topic
# ------------------------------------------------
@mcp.tool()
async def get_news_by_topic(
    topic: str,
    language: str = "en",
    max_results: int = 5
) -> str:
    """
    Fetch news by topic.
    """

    topic = topic.strip().lower()

    logger.info(f"Fetching topic: {topic}")

    allowed_topics = [
        "breaking-news",
        "world",
        "nation",
        "business",
        "technology",
        "entertainment",
        "sports",
        "science",
        "health"
    ]

    if topic not in allowed_topics:

        return (
            f"Unsupported topic '{topic}'. "
            f"Allowed topics: "
            f"{', '.join(allowed_topics)}"
        )

    params = {
        "topic": topic,
        "lang": language,
        "max": max_results
    }

    return await fetch_news(
        "top-headlines",
        params
    )


# ------------------------------------------------
# Tool 4: News By Date Range
# ------------------------------------------------
@mcp.tool()
async def get_news_by_date_range(
    query: str,
    from_date: str,
    to_date: str,
    max_results: int = 5,
    language: str = "en"
) -> str:
    """
    Fetch news within date range.
    """

    query = query.strip()

    logger.info(
        f"Fetching news from "
        f"{from_date} to {to_date}"
    )

    if not query:
        return "Search query cannot be empty."

    try:

        from_dt = datetime.strptime(
            from_date,
            "%Y-%m-%d"
        )

        to_dt = datetime.strptime(
            to_date,
            "%Y-%m-%d"
        )

    except ValueError:

        return (
            "Invalid date format. "
            "Use YYYY-MM-DD"
        )

    if from_dt > to_dt:

        return (
            "Error: from_date must be "
            "earlier than to_date."
        )

    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "lang": language,
        "max": max_results
    }

    return await fetch_news(
        "search",
        params
    )


# ------------------------------------------------
# Run MCP Server
# ------------------------------------------------
if __name__ == "__main__":
    mcp.run()