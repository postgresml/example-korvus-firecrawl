from korvus import Collection, Pipeline
from firecrawl import FirecrawlApp
import os
import time
import asyncio
from rich import print
from rich.pretty import pprint
from dotenv import load_dotenv
import argparse


# Load variables from our .env file
load_dotenv()


# Configure our program args
parser = argparse.ArgumentParser(description="Example Korvus x Firecrawl")
parser.add_argument(
    "action", choices=["crawl", "search", "rag"], help="Action to perform"
)


# Initialize the FirecrawlApp with your API key
firecrawl = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])


# Define our Pipeline and Collection
pipeline = Pipeline(
    "v0",
    {
        "markdown": {
            "splitter": {"model": "markdown"},
            "semantic_search": {
                "model": "mixedbread-ai/mxbai-embed-large-v1",
            },
        },
    },
)
collection = Collection(
    "korvus-firecrawl-example-0", database_url=os.environ["KORVUS_DATABASE_URL"]
)


# Add our Pipeline to our Collection
async def add_pipeline():
    await collection.add_pipeline(pipeline)


# Crawl with Firecrawl
def crawl():
    print("Crawling...")
    job = firecrawl.crawl_url(
        os.environ["CRAWL_URL"],
        params={
            "limit": int(os.environ["CRAWL_LIMIT"]),
            "scrapeOptions": {"formats": ["markdown"]},
        },
        poll_interval=30,
    )
    return job


# Do RAG
async def do_rag(user_query):
    results = await collection.rag(
        {
            "CONTEXT": {
                "vector_search": {
                    "query": {
                        "fields": {
                            "markdown": {
                                "query": user_query,
                                "parameters": {
                                    "prompt": "Represent this sentence for searching relevant passages: "
                                },
                            }
                        },
                    },
                    "document": {"keys": ["id"]},
                    "rerank": {
                        "model": "mixedbread-ai/mxbai-rerank-base-v1",
                        "query": user_query,
                        "num_documents_to_rerank": 100,
                    },
                    "limit": 5,
                },
                "aggregate": {"join": "\n\n\n"},
            },
            "chat": {
                "model": "meta-llama/Meta-Llama-3.1-405B-Instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a question and answering bot. Answer the users question given the context succinctly.",
                    },
                    {
                        "role": "user",
                        "content": f"Given the context\n\n:{{CONTEXT}}\n\nAnswer the question: {user_query}",
                    },
                ],
                "max_tokens": 256,
            },
        },
        pipeline,
    )
    return results


# Do search
async def do_search(user_query):
    results = await collection.search(
        {
            "query": {
                "semantic_search": {
                    "markdown": {
                        "query": user_query,
                    },
                },
            },
            "limit": 5,
        },
        pipeline,
    )
    return results


# Get user input and call our callback
async def input_loop(callback):
    while True:
        query = input("Enter your query (or 'q' to quit): ")
        if query.lower() == "q":
            break
        results = await callback(query)
        print("\n[bold]Results:[/bold]\n")
        pprint(results, max_length=2, max_string=100)


# Our main function
async def main():
    args = parser.parse_args()

    if args.action == "crawl":
        # Add our Pipeline to our Collection
        # We only ever need to do this once
        # Calling it more than once does nothing
        await add_pipeline()

        # Crawl the website
        results = crawl()

        # Construct our documents to upsert
        documents = [
            {"id": data["metadata"]["sourceURL"], "markdown": data["markdown"]}
            for data in results["data"]
        ]

        # Upsert our documents
        await collection.upsert_documents(documents)

    elif args.action == "rag":
        await input_loop(do_rag)

    elif args.action == "search":
        await input_loop(do_search)


asyncio.run(main())
