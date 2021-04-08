from dotenv import load_dotenv
import requests
from datetime import datetime
import smtplib
import os
load_dotenv()
TOKEN = os.environ.get("token")
USER = os.environ.get("user")
pixela_endpoint = "https://pixe.la/v1/users"

requestHeader = {
    "X-USER-TOKEN": TOKEN
}
user_params = {
    "token": TOKEN,
    "username": USER,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes"
}
graphID = "graph1"


pixela_endpoint = "https://pixe.la/v1/users"
graph_endpoint = "{}/{}/graphs".format(pixela_endpoint, USER)



user_params = {
    "token": TOKEN,
    "username": USER,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes"
}

# create a user:
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)
#print(response.status_code)
# Graphs

#get all graphs

request_graph = requests.get(url=graph_endpoint, headers=requestHeader)
#print(request_graph.text)
json = request_graph.json()
graph_dict = {json.get("graphs")[i].get("name"):json.get("graphs")[i] for i in range(len(json.get("graphs")))}
command = input("Would you like to add to an existing graph, create a new graph or delete one?(ADD/CREATE/DELETE)\n")
if command == "ADD" and len(graph_dict) != 0:
    print("In which graph would you like to append?")
    i=1
    idDict = {}
    for k,v in graph_dict.items():
        print("{}. {}".format(i, k))
        idDict[str(i)] = k
        i += 1
    #print(idDict)
    idToAppend = str(input("Number of the graph: "))
    scopedGraph = graph_dict.get(idDict.get(idToAppend))
    command = input("Would you like to commit today or update a previous day?(TODAY/PREVIOUS)\n")
    if command == "TODAY":
        date = datetime.now()
        date = date.strftime('%Y%m%d')
        spentTime = input("How much {} you spent: \n".format(scopedGraph.get('unit')))
        add_value = {
            "date": date,
            "quantity": spentTime
        }
        add_endpoint = "{}/{}".format(graph_endpoint, scopedGraph.get("id"))
        response = requests.post(url=add_endpoint, json=add_value, headers=requestHeader)
        print(response.text)
    elif command == "PREVIOUS":
        date = input("The day you want to update(YYYY-MM-DD) : ")
        date = str(date).replace("-", "")
        spentTime = input("How much {} you spent: \n".format(scopedGraph.get('unit')))
        update_value = {
            "date": date,
            "quantity": spentTime
        }
        add_endpoint = "{}/{}".format(graph_endpoint, scopedGraph.get("id"))
        update_endpoint = "{}/{}".format(add_endpoint, date)
        response = requests.put(url=update_endpoint, json=update_value, headers=requestHeader)
        print(response.text)
    else:
        print("Unknown command {}".format(command))
elif command == "CREATE":
    graphID = input("Please enter your graph ID:\n")
    graphName = input("Please enter your graph name:\n")
    graphUnit = input("Please enter the unit you want:\n")
    graphType = input("Please enter the type(int/float):\n")
    color = input("Please enter the color\nshibafu (green), momiji (red), sora (blue), ichou (yellow), ajisai (purple) and kuro (black):\n")
    graph_config = {
        "id" : graphID,
        "name": graphName,
        "unit" : graphUnit,
        "type": graphType,
        "color": "sora"

    }
    response = requests.post(url=graph_endpoint, json=graph_config, headers=requestHeader)
    print(response.text)
elif command == "DELETE":
    print("Which graph would you like to delete?")
    i = 1
    idDict = {}
    for k, v in graph_dict.items():
        print("{}. {}".format(i, k))
        idDict[str(i)] = k
        i += 1
    # print(idDict)
    idToAppend = str(input("Number of the graph: "))
    scopedGraph = graph_dict.get(idDict.get(idToAppend))
    delete_endpoint = "{}/{}".format(graph_endpoint, scopedGraph.get("id"))
    if str(input("Are you sure you want to delete it? Type 'DELETE' to proceed:\n")) == "DELETE":
        response = requests.delete(url=delete_endpoint, headers=requestHeader)
        print(response.text)