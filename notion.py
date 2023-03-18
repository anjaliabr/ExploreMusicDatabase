import requests
import json

NOTION_TOKEN = "secret_X6CLplBBBIer2q2qFGvNUdkte2z4JMmiYkPBlJt2TPa"
SONGS_DATABASE_ID = "2e33b124b697426b801bdd003b2ec2fd"
ALBUMS_DATABASE_ID = "d65235a6621a4e629727841a4d89d7ba"
ARTISTS_DATABASE_ID = "34e5ed1507d9451e829684f2a499d04d"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def readDatabase(databaseID, name):
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open(f'./{name}.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def createPage(data):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {data}
            
    }
    
    data_dump = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data_dump)

    print(res.status_code)
    print(res.text)

readDatabase(SONGS_DATABASE_ID, "songs")
readDatabase(ALBUMS_DATABASE_ID, "albums")
readDatabase(ARTISTS_DATABASE_ID, "artists")

data = {
    "Album": {"relation": [{"text": {"content": "Nectar"}}]},
    "Year": {"number": []}
}
#createPage