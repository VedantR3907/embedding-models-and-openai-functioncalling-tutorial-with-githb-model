import os
import json
from openai import OpenAI
from datetime import datetime

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"


def order_food(food_item: str):
    current_date_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    if 'pizza' in food_item.lower():
        return  json.dumps({
            'Food':food_item,
            'Cost':'$22',
            'order_time': current_date_time
        })
    elif 'burger' in food_item.lower():
        return  json.dumps({
            'Food':food_item,
            'Cost':'$10',
            'order_time': current_date_time
        })
    elif 'nachos' in food_item.lower():
        return  json.dumps({
            'Food':food_item,
            'Cost':'$15',
            'order_time': current_date_time
        })
    else:
        return  json.dumps({
            'Food': 'No food ordered. Please order a food to proceed.'
        })

tool = {
    "type": "function",
    "function": {
        "name": "order_food",
        "description": """Returns the food details of the customer ordered food with price, food name and the time and date the food was ordered""",
        "parameters":{
            "type": "object",
            "properties": {
                "food_item": {
                    "type": "string",
                    "description": """The name of the food item to be ordered by the customer."""
                }
            },
            "required":[
                "food_item"
            ]
        }
    }
}

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

messages=[
    {"role": "system", "content": "You an assistant that helps customers order food items. Only answer the customer query if it is orederd food. Else reply with 'CHUP BKLE'. If the food is not on the menu plase make the bill for the other food items on the menu and write message for the food item as 'the {food item} is not on the menu today'. Also if multiple orders are made then please make sure to give the total bill to the customer."},
    {"role": "user", "content": "Hi! Hows your day?"},
]


response = client.chat.completions.create(
    messages=messages,
    tools=[tool],
    model=model_name,
)
print(response)

if response.choices[0].finish_reason == 'tool_calls':
    messages.append(response.choices[0].message)

    if response.choices[0].message.tool_calls:

        tool_call = response.choices[0].message.tool_calls

        for i in tool_call:

            if i.type == "function":
                function_args = json.loads(i.function.arguments)
                callable_func = locals()[i.function.name]
                function_return = callable_func(**function_args)

                messages.append(
                    {
                        "tool_call_id": i.id,
                        "role": "tool",
                        "name": i.function.name,
                        "content": function_return,
                    }
                )

        response = client.chat.completions.create(
            messages=messages,
            tools=[tool],
            model=model_name,
        )

        print(f"{response.choices[0].message.content}")
else:
    print(response.choices[0].message.content)

'''ChatCompletion(id='chatcmpl-A871SU4ypgwnPGF8bn90zFxTMfBYT', 
choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, 
message=ChatCompletionMessage(content=None, refusal=None, role='assistant', 
function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_vEt3mubzDvIBh2fGLL0d48Ic', 
function=Function(arguments='{"food_item": "cheesy nachos"}', name='order_food'), type='function'), 
ChatCompletionMessageToolCall(id='call_kDEuJTQPCfviMqWlqXvdEwne', 
function=Function(arguments='{"food_item": "margarita pizza"}', name='order_food'), type='function')]))], created=1726496982, model='gpt-4o-2024-08-06', object='chat.completion', service_tier=None, system_fingerprint='fp_b2ffeb16ee', usage=CompletionUsage(completion_tokens=52, prompt_tokens=127, total_tokens=179))'''

'''ChatCompletion(id='chatcmpl-A872YlT2yVoPtmpY33rG0afCqV37K', 
choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, 
message=ChatCompletionMessage(content=None, refusal=None, role='assistant', 
function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_ymVpM3RrhymgKZdBPYFuwup5', 
function=Function(arguments='{"food_item":"Margherita Pizza"}', name='order_food'), type='function')]))], created=1726497050, model='gpt-4o-2024-08-06', object='chat.completion', service_tier=None, system_fingerprint='fp_b2ffeb16ee', usage=CompletionUsage(completion_tokens=18, prompt_tokens=122, total_tokens=140))'''