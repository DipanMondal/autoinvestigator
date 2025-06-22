from flask import Flask,request,jsonify
from dotenv import load_dotenv
from tools.web_search import WebSearchTool

app=Flask(__name__)

web_searcher = WebSearchTool()

@app.route('/web-search',methods=['POST'])
def web_search():
    data = request.get_json()
    print(data)
    
    try:
        name = data["company_name"]
        results = web_searcher.run(query=name, num_results=5)
        return jsonify({"results": results})
    except KeyError:
        return jsonify({"error":"There is no 'company_name' in your request"})
    except Exception:
        return jsonify({"error":"Something went wrong. Can't search the web"})
       
    return jsonify({"message":f"{name}"})
    

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)