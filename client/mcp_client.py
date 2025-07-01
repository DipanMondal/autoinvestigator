import requests
import json
import uuid

class MCPClient:
    """
    A client for interacting with the MCP (Multi-Agent Control Plane) server,
    built to match the specific request/response format of server.py.
    """

    def __init__(self, server_url="http://127.0.0.1:5000"):
        """
        Initializes the MCPClient with the server's URL.
        """
        self.server_url = server_url
        self.headers = {"Content-Type": "application/json"}

    def _send_request(self, requests_list):
        """
        Private helper method to send a fully constructed request object to the server.
        
        Args:
            requests_list (list): A list of formatted request dictionaries.
        
        Returns:
            dict: The JSON response from the server.
        """
        # Build the final payload with a main ID and the list of requests
        payload = {
            "id": str(uuid.uuid4()),
            "requests": requests_list
        }

        try:
            print("\n--- Sending Payload ---")
            print(json.dumps(payload, indent=2))
            print("----------------------")

            response = requests.post(
                f"{self.server_url}/requests",
                headers=self.headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while communicating with the server: {e}")
            if e.response:
                print("Server response:", e.response.text)
            return None

    def execute_tool(self, method, params={}):
        """
        Constructs and sends a request for a single tool or prompt.
        
        Args:
            method (str): The method string, e.g., "tools/websearch" or "prompt/list".
            params (dict, optional): The parameters for the tool. Defaults to {}.

        Returns:
            dict: The JSON response from the server.
        """
        # Each individual request needs its own ID and the correct structure
        single_request = {
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params
        }
        
        # The _send_request method expects a list of requests
        return self._send_request([single_request])


if __name__ == '__main__':
    # This block demonstrates how to use the updated client
    mcp_client = MCPClient()

    # --- Example 1: Web Search (tools/websearch) ---
    print("\n--- Testing Web Search Tool ---")
    # Note the new method name from your server.py: "websearch" not "web_search"
    search_result = mcp_client.execute_tool("tools/websearch", {"query": "Latest news on Google Gemini"})
    if search_result:
        print("Web Search Result:", json.dumps(search_result, indent=2))
    print("-" * 30)
    
    # --- Example 2: News (tools/news) ---
    print("\n--- Testing News Tool ---")
    # Note the parameter name from your server.py: "name"
    news_result = mcp_client.execute_tool("tools/news", {"name": "Nvidia"})
    if news_result:
        print("News Scanner Result:", json.dumps(news_result, indent=2))
    print("-" * 30)

    # --- Example 3: List available tools (tools/list) ---
    print("\n--- Testing List Tools ---")
    tools_list = mcp_client.execute_tool("tools/list")
    if tools_list:
        print("Available Tools:", json.dumps(tools_list, indent=2))
    print("-" * 30)

    # --- Example 4: Get a prompt template (prompt/request_template) ---
    print("\n--- Testing Get Prompt Template ---")
    prompt_template = mcp_client.execute_tool("prompt/request_template")
    if prompt_template:
        print("Prompt Template:", json.dumps(prompt_template, indent=2))
    print("-" * 30)