# Korvus x Firecrawl Example

This example application demonstrates how to perform web crawling, semantic search, and Retrieval-Augmented Generation (RAG) using [Korvus](https://github.com/postgresml/korvus) and [Firecrawl](https://www.firecrawl.dev/).

## Features

- Web crawling using Firecrawl
- Semantic search over crawled content
- RAG (Retrieval-Augmented Generation) for question answering

## Prerequisites

- Python 3.7+
- Firecrawl API key
- PostgresML database URL

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/korvus-firecrawl-example.git
   cd korvus-firecrawl-example
   ```

2. Install the required packages:
   ```
   pip install korvus firecrawl python-dotenv rich
   ```

3. Create a `.env` file in the project root and add your credentials:
   ```
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   KORVUS_DATABASE_URL=your_postgresml_database_url
   CRAWL_URL=https://example.com
   CRAWL_LIMIT=100
   ```

## Usage

The application supports three main actions: crawl, search, and rag.

1. Crawl a website:
   ```
   python main.py crawl
   ```

2. Perform semantic search:
   ```
   python main.py search
   ```

3. Use RAG for question answering:
   ```
   python main.py rag
   ```

For search and RAG, you'll be prompted to enter queries. Type 'q' to quit the input loop.

## How it works

1. The application uses Firecrawl to crawl the specified website and extract markdown content.
2. Crawled data is processed and stored using Korvus.
3. Semantic search allows you to find relevant documents based on your queries.
4. RAG combines retrieved context with a language model to answer questions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
