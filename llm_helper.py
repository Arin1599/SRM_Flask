def get_llm_response_mini(prompt, system_prompt="You are an AI assistant."):
    import os
    import requests
    import json
    url = 'https://tslopenabackend.azurewebsites.net/openaicall'
    messages = [
        {"role": "system","content": f"{system_prompt}"},
        {"role": "user", "content": f"{prompt}"}
                ]
    payload = {
    'deployment_name': "gpt-4o-mini", #"gemini-1.5-flash", #" #For GPT 4: tsl-gpt4-turbo////gemini-1.5-flash
    'temperature': '0.3',
    'adid': '199325', #e.g ‘80xxxx’
#     'application_name':'Weekly Insights',
    'apikey':'703H7354D37982BJ' ,#e.g, “”
    'messages': json.dumps(messages),
    'max_tokens': '8192'}
    # headers = {'jwt-token':interim_code}
    final_gpt_response = requests.request("POST", url, data=payload)
    return final_gpt_response.text

def get_llm_response(prompt):
    import os
    import requests
    import json
    
    url = 'https://tslopenabackend.azurewebsites.net/openaicall'
    messages = [
        {"role": "user", "content": f"{prompt}"}
    ]
    payload = {
        'deployment_name': "gpt-o1",
        'temperature': '0.3',
        'adid': '199325',
        'apikey': '703H7354D37982BJ',
        'messages': json.dumps(messages),
        'max_tokens': '8192'
    }
    
    final_gpt_response = requests.request("POST", url, data=payload)
    
    # Check if the response is successful
    if final_gpt_response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            response_json = final_gpt_response.json()
            return response_json['choices'][0]['message']['content']
        except json.JSONDecodeError as e:
            print("JSON decoding failed:", e)
            print("Response text:", final_gpt_response.text)
            return None
    else:
        print("Request failed with status code:", final_gpt_response.status_code)
        print("Response text:", final_gpt_response.text)
        return None
