import requests
import json

def render_response(status, code, message, data):
    return {
        "status": status,
        "code": code,
        "message": message,
        "data": data
    }

def main(trello_api_key, trello_token, trello_username, trello_url, trello_list_name, trello_card_fields):
    # Step 1 ______________________________________________________________________________________________________
    # Get all boards information using username
    board_id = "" 
    
    get_boards_url = "https://api.trello.com/1/members/"+ trello_username +"/boards?key="+ trello_api_key +"&token="+ trello_token +"&fields=name,shortLink,url"
    boards_response = requests.request("GET", get_boards_url)
    
    try:
        boards_json_response = boards_response.json()
    except ValueError, e:
        return render_response(
            400, 
            "INVALID_KEY_TOKEN_USERNAME", 
            "Invalid specified Trello Key/Token/Username", 
            ""
        )
    
    #Get the board ID based on the specified Trello URL
    for response in boards_json_response:
        if response["url"] == trello_url:
            board_id = response["id"]
            break

    if not board_id:
        # Return Invalid URL
        return render_response(
            400, 
            "INVALID_TRELLO_URL", 
            "Invalid specified Trello URL", 
            ""
        )


    # Step 2 ______________________________________________________________________________________________________
    # Get all lists of the board
    list_id = ""
    get_lists_url = "https://api.trello.com/1/boards/"+ board_id +"/lists?key="+ trello_api_key +"&token="+ trello_token +"&fields=name"
    lists_response = requests.request("GET", get_lists_url)
    
    try:
        lists_json_response = lists_response.json()
    except ValueError, e:
        return render_response(
            400, 
            "INVALID_KEY_TOKEN", 
            "Invalid specified Trello Key/Token", 
            ""
        )

    #Get the list ID based on the specified Trello List Name
    for response in lists_json_response:
        if response["name"] == trello_list_name:
            list_id = response["id"]
            break

    if not list_id:
        # Return Invalid List Name
        return render_response(
            400, 
            "INVALID_LIST_NAME", 
            "Invalid specified Trello List Name or Column Name", ""
        )


    # Step 3 ______________________________________________________________________________________________________
    # Get all cards inside the list

    get_cards_url = "https://api.trello.com/1/lists/"+ list_id +"/cards?fields="+ trello_card_fields +"&key="+ trello_api_key +"&token="+ trello_token
    cards_response = requests.request("GET", get_cards_url)

    try:
        cards_json_response = cards_response.json()
    except ValueError, e:
        return render_response(
            400, 
            "INVALID_KEY_TOKEN", 
            "Invalid specified Trello Key/Token", 
            ""
        )

    # SUCCESS!!!
    return render_response(
        200, 
        "SUCCESS", 
        "Request was successfully performed", 
        cards_json_response
    )

