from typing import List, Type, Union
from openai import OpenAI
from instructor.client import Instructor
from pydantic import BaseModel
from functools import partial

prompt = {
  "role": "system",
  "content": """You will be provided the data entry of a person, which includes the city and country of origin of the person

You are tasked to extract the following information, with the following requirement

1. "city": The city in the person's address entry. 
Please format your answer according to the following requirements
- Remove spelling mistakes (e.g. correct Bosston to Boston)
- Change to correct formatting (e.g. correct houston to Houston, capitalizing the initial "H")
- Change to full spelling (e.g. correct PDX to Portland)

2. "state": The state which the person lives in, please determine the information using the city that they are from
Please format your answer according to the following requirements
- Return a (two letter) state and territory abbreviation, for example, if someone is from Minneapolis (some city in Minnesota), you will answer with "MN", which is the correct abbreviation for Minnesota
- If the state cannot be determined, please fill that entry with "Unknown" (without the quotation marks)


Your response should be in JSON format with two fields:
* city: The city in the person's address entry, with the correct format
* state: The state which the person resides in.

Example response format:
{"city": "Minneapolis", "state": "Minnesota"}

Ensure your response is a single-line JSON object."""
}

class CityAndState(BaseModel):
    city: str
    state: str
    
def get_structured_response(messages: List[dict],
                            response_model: Type[BaseModel] = None,
                            return_fields: List[str]| str | None = ["response"],
                            single_item_list_return_dict: bool = False,
                            client: Instructor = None,
                            client_args: dict = dict(),
                            verbose: bool = False,
                            **kwargs):
    response: BaseModel = client.chat.completions.create(
        response_model = response_model,
        messages = messages,
        **client_args
    )
    stripped_response = response_fields(response, return_fields, single_item_list_return_dict)
    return stripped_response
  
def response_fields(response: BaseModel, return_fields: List[str]| str | None, single_item_list_return_dict: bool):
    if return_fields is None or len(return_fields) == 0:
        return response

    if isinstance(return_fields, str):
        return getattr(response, return_fields)

    if len(return_fields) == 1 and not single_item_list_return_dict:
        return getattr(response, return_fields[0])

    return {field: getattr(response, field) for field in return_fields}

def get_city_and_state_func(client: Instructor, client_args: dict = dict()):
    def city_and_state_func(doc: dict):
        response_func = partial(get_structured_response, 
                                response_model = CityAndState, 
                                return_fields = ["city", "state"],
                                client = client, 
                                client_args = client_args)
        usr_msg = {
            "role": "user",
            "content": f"The following is the relevant entry: \n {str(doc)}"
        }
        msg_history = [prompt, usr_msg]
        response: dict = response_func(messages=msg_history)
        return {"address": {"city": response["city"], "state": response["state"]}}
    return city_and_state_func
        