import requests

# Replace with your actual API key and external user ID
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
external_user_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Amazon Agent Code to query for laptops
create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
headers = {
    'apikey': api_key
}
create_session_body = {
    "pluginIds": [],
    "externalUserId": external_user_id
}

# Step 1: Create a session for Amazon agent
response = requests.post(create_session_url, headers=headers, json=create_session_body)

if response.status_code == 201:
    session_id = response.json()['data']['id']
    print(f"Session created with ID: {session_id}")

    # Submit Query to Amazon agent (laptops under 60,000 price)
    submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    submit_query_body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": "samsung phone below 15000 price ",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1716334779"],
        "responseMode": "sync"
    }

    response = requests.post(submit_query_url, headers=headers, json=submit_query_body)

    if response.status_code == 200:
        print("Query submitted successfully.")
        amazon_response = response.json()
        print("Amazon Agent Response:", amazon_response)

        # Extract the 'answer' key for the body content
        amazon_output = amazon_response['data']['answer']
        print("Amazon Output:", amazon_output)

        # Step 2: Use the Amazon agent's output as email body
        # Create a session for email agent
        create_session_body = {
            "pluginIds": [],
            "externalUserId": external_user_id
        }
        response = requests.post(create_session_url, headers=headers, json=create_session_body)

        if response.status_code == 201:
            session_id = response.json()['data']['id']
            print(f"Email session created with ID: {session_id}")

            # Submit email query
            submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
            submit_query_body = {
                "endpointId": "predefined-openai-gpt4o",
                "query": f"send mail to bharathmunakala22@gmail.com with body '{amazon_output}' and subject: 'Amazon'",
                "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1722285968"],
                "responseMode": "sync"
            }

            query_response = requests.post(submit_query_url, headers=headers, json=submit_query_body)

            if query_response.status_code == 200:
                print("Query submitted successfully for sending email.")
                print("Response:", query_response.json())
            else:
                print("Failed to submit email query. Status Code:", query_response.status_code)
        else:
            print("Failed to create email session. Status Code:", response.status_code)
    else:
        print("Failed to submit query to Amazon agent:", response.status_code, response.text)
else:
    print("Failed to create session:", response.status_code, response.text)
