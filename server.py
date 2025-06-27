from flask import Flask,request,jsonify
from dotenv import load_dotenv


app=Flask(__name__)


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
            method: "tools/<tool_name>",
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

from server.interface import UTIL

util = UTIL()

def request_handler(request):
    try:
        id = request['id'] if 'id' in request else None
        response = {'id':id, 'results':[]}
        
        for req in request['requests']:
            res = {}
            res['id'] = req['id']
            res['method'] = req['method']
            n, method = req['method'].strip().split('/') 
            
            if n=='tools':
                if method == "websearch":
                    query = req['params']['query']
                    ans = util.get_web_search(query)
                    res['results'] = [ans]
                elif method == "financial_descriptor":
                    ticker = req['params']['ticker']
                    cik = req['params']['cik']
                    ans = util.get_financial_data(ticker=ticker,cik=cik)
                    res['results'] = [ans]
                elif method == "news":
                    name = req['params']['name']
                    ans = util.get_news(name=name)
                    res['results'] = [util.get_news(name=name)]
                elif method == "send_mail":
                    subject = req['params']['subject']
                    message = req['params']['message']
                    receiver = req['params']['receiver']
                    res['results']=[util.send_mail(subject=subject, message=message, receiver=receiver)]
            elif n=="prompt":
                pass
            
            elif n=="resources":
                pass
                
            response['results'].append(res)
        return response
    except Exception as e:
        raise e
        return {"message":"Bad Request. Please check the format"}


@app.route('/requests',methods=['POST'])
def base():
    data = request.get_json()
    print(data)
    res = request_handler(data)
    return jsonify(res)
    
   

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)