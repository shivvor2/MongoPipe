# MongoDB Data Processing Pipeline

This project demonstrates a flexible data processing pipeline for MongoDB collections. It allows you to define a series of operations to be applied to documents in a source collection and store the results in a destination collection.

## Features

- Process MongoDB documents through a customizable pipeline of operations
- Support for both hard-coded and LLM-assisted data transformations
- Easy comparison between source and processed documents

## Usage

1. Start your MongoDB server.

2. Define your processing operations. Example operations are provided in the `demo_func` directory.

3. Create your pipeline:

```python
from pymongo import MongoClient
from mongopipe.mongopipe import MongoPipe
from mongopipe.demo_func.demo_funcs import identity, cap_interests, correct_city_and_state 

# Set up MongoDB connections
client = MongoClient("mongodb://localhost:27017")
source_collection = client["source_db"]["source_collection"]
dest_collection = client["dest_db"]["processed_collection"]

# Define operations
ops = [identity, cap_interests, correct_city_and_state]

# Create and run the pipeline
pipe_instance = MongoPipe(source=source_collection, destination=dest_collection, ops=ops)
pipe_instance.run()
```

4. Compare the results:

```python
from mongopipe.utils import compare_entries

compare_entries(source_collection, dest_collection, document_id)
```

## LLM-Assisted Operations

Below is a demo on Import and set up the LLM-assisted operations:

:

```python
from dotenv import load_dotenv
import os
import instructor
from openai import OpenAI
from demo_func.get_city_and_state_llm import get_city_and_state_func

load_dotenv()

client_args = {
    "model": "meta-llama/llama-3.2-3b-instruct",
    "temperature": 0.3,
}

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

structured_client = instructor.from_openai(client, mode=instructor.Mode.JSON)

correct_city_and_state_llm = get_city_and_state_func(structured_client, client_args)

# Use this function in your pipeline operations
ops = [identity, cap_interests, correct_city_and_state_llm]
```
