from flask import Flask,request,jsonify
from dotenv import load_dotenv
from server.tools.web_search import WebSearchTool

app=Flask(__name__)

web_searcher = WebSearchTool()

"""
Basic Request Format:
{
    id : <id>,
    requests:[
        {
            id:<request_id>,
            method : "tools/<tool_name>",
            params : {
                param1:value1,
                param2:value2,
                ...
            }
        },
        {
            id:<request_id>,
            method : "tools/<tool_name>",
            params : {
                param1:value1,
                param2:value2,
                ...
            }
        },
        ...
    ]
}

Basic Response Format:
{
    id:<id>
    results:[
        {
            id:<request_id>,
            method: "tools/<tool_name>,
            results:[...]
        },
        {
            id:<request_id>,
            method: "tools/<tool_name>,
            results:[...]
        },
        ...
    ]
}
"""


@app.route('/web-search',methods=['POST'])
def web_search():
    data = request.get_json()
    print(data)
    
    try:
        name = data["company_name"]
        query = f"Detail Company profile of {name} company profile site:investopedia.com OR site:crunchbase.com OR site:forbes.com OR site:finance.yahoo.com OR site:sec.gov"
        results = web_searcher.run(query=query, num_results=5)
        return jsonify({"results": results})
    except KeyError:
        return jsonify({"error":"There is no 'company_name' in your request"})
    except Exception as e:
        print(str(e))
        return jsonify({"error":"Something went wrong. Can't search the web"})
       
    return jsonify({"message":f"{name}"})
    

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)