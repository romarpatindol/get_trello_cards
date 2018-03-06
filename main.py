import requests
import json


class GetTrelloCards:
    def __init__(self, trello_api_key, trello_token, trello_username, trello_url, trello_list_name, trello_label_name, trello_card_fields):
        self.trello_api_key = trello_api_key
        self.trello_token = trello_token
        self.trello_username = trello_username
        self.trello_url = trello_url
        self.trello_list_name = trello_list_name
        self.trello_label_name = trello_label_name
        self.trello_card_fields = trello_card_fields
        self.board_id = ""
        self.list_id = ""
        self.board_label_id = ""
        self.list_container = {}
        self.response_value = []

    def render_response(self, status, code, message, data):
        return {
            "status": status,
            "code": code,
            "message": message,
            "data": data
        }

    def get_lists(self):
        # Step 2 ______________________________________________________________________________________________________
        # Get all lists of the board
        list_id = ""
        get_lists_url = "https://api.trello.com/1/boards/"+ self.board_id +"/lists?key="+ self.trello_api_key +"&token="+ self.trello_token +"&fields=name"
        lists_response = requests.request("GET", get_lists_url)
        
        try:
            lists_json_response = lists_response.json()
        except ValueError, e:
            return self.render_response(
                400, 
                "INVALID_KEY_TOKEN", 
                "Invalid specified Trello Key/Token", 
                ""
            )

        #Get the list ID based on the specified Trello List Name
        for response in lists_json_response:
            if response["name"] in self.trello_list_name:
                list_id = response["id"]
                list_name = response["name"]
                self.list_container[list_name] = list_id

        if not list_id:
            # Return Invalid List Name
            return self.render_response(
                400, 
                "INVALID_LIST_NAME", 
                "Invalid specified Trello List Name or Column Name", ""
            )

        #Initialize List ID
        self.list_id = list_id
        return self.render_response(
            200,
            "SUCCESSFUL", 
            "Request successfully performed",
            ""
        )

    def get_board_label_id(self):
        board_label_id = ""
        get_labels_url = "https://api.trello.com/1/boards/"+ self.board_id +"/labels?key="+ self.trello_api_key +"&token="+ self.trello_token +"&fields=name"
        labels_response = requests.request("GET", get_labels_url)
        
        try:
            labels_json_response = labels_response.json()
        except ValueError, e:
            return self.render_response(
                400, 
                "INVALID_KEY_TOKEN_USERNAME", 
                "Invalid specified Trello Key/Token/Username", 
                ""
            )
        
        #Get the board ID based on the specified Trello URL
        for response in labels_json_response:
            if response["name"].lower() == self.trello_label_name.lower():
                board_label_id = response["id"]
                break

        if not board_label_id:
            # Return Invalid URL
            return self.render_response(
                400, 
                "INVALID_LABEL_NAME", 
                "Invalid specified Label Name", 
                ""
            )
        
        # Initialize Board ID
        self.board_label_id = board_label_id
        return self.render_response(
            200,
            "SUCCESSFUL", 
            "Request successfully performed",
            ""
        )

    def get_board_id(self):
        board_id = ""
        get_boards_url = "https://api.trello.com/1/members/"+ self.trello_username +"/boards?key="+ self.trello_api_key +"&token="+ self.trello_token +"&fields=name,shortLink,url"
        boards_response = requests.request("GET", get_boards_url)
        
        try:
            boards_json_response = boards_response.json()
        except ValueError, e:
            return self.render_response(
                400, 
                "INVALID_KEY_TOKEN_USERNAME", 
                "Invalid specified Trello Key/Token/Username", 
                ""
            )
        
        #Get the board ID based on the specified Trello URL
        for response in boards_json_response:
            if response["url"] == self.trello_url:
                board_id = response["id"]
                break

        if not board_id:
            # Return Invalid URL
            return self.render_response(
                400, 
                "INVALID_TRELLO_URL", 
                "Invalid specified Trello URL", 
                ""
            )
        
        # Initialize Board ID
        self.board_id = board_id
        return self.render_response(
            200,
            "SUCCESSFUL", 
            "Request successfully performed",
            ""
        )

    def get_cards(self):
        # Step 3 ______________________________________________________________________________________________________
        # Get all cards inside the list

        for key in self.list_container.keys():
            get_cards_url = "https://api.trello.com/1/lists/"+ self.list_container[key] +"/cards?fields="+ self.trello_card_fields +"&key="+ self.trello_api_key +"&token="+ self.trello_token
            cards_response = requests.request("GET", get_cards_url)
            cards = []
            try:
                cards_json_response = cards_response.json()
                for response in cards_json_response:
                    if self.board_label_id in response["idLabels"]:
                        cards.append(response)
                
                self.response_value.append(
                    {
                        "list_name": key,
                        "cards": cards
                    }
                )

            except ValueError, e:
                return self.render_response(
                    400, 
                    "INVALID_KEY_TOKEN", 
                    "Invalid specified Trello Key/Token", 
                    ""
                )

        # SUCCESS!!!
        return self.render_response(
            200, 
            "SUCCESS", 
            "Request was successfully performed",
            ""
        )

    def get(self):
        # Step 1 ______________________________________________________________________________________________________
        # Get all boards information using username
        board_response = self.get_board_id()
        if board_response["status"] == 400:
            return board_response

        lists_response = self.get_lists()
        if lists_response["status"] == 400:
            return lists_response

        label_response = self.get_board_label_id()
        if label_response["status"] == 400:
            return label_response

        cards_response = self.get_cards()
        if cards_response["status"] == 400:
            return cards_response
        
        return self.response_value

def main(trello_api_key, trello_token, trello_username, trello_url, trello_list_name, trello_label_name, trello_card_fields):
    split_list_name = trello_list_name.split(",")
    split_list_name = map(str.strip, split_list_name)
    get_trello_cards = GetTrelloCards(
        trello_api_key=trello_api_key,
        trello_token=trello_token,
        trello_username=trello_username,
        trello_url=trello_url,
        trello_list_name=split_list_name,
        trello_label_name=trello_label_name,
        trello_card_fields=trello_card_fields
    )
    return get_trello_cards.get()
