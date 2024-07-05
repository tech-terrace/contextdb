import requests
from fastapi import HTTPException



def get_embedding(url: str, query: str, num_of_results: int = 10) -> list[str]:
    import chromadb
    
    client = chromadb.PersistentClient(path="chroma")
    
    # example of url https://storage.googleapis.com/contextdb/docfiles/fast-api0.111.0_large.txt"
    if 'https://storage.googleapis.com/contextdb/docfiles/' not in url:
        raise HTTPException(status_code=400, detail="Invalid URL")
    collection_name = url.split('/')[-1].replace('.txt', '')
    try:
        collection = client.get_collection(collection_name)
    except Exception as e:
        try:
            collection = client.create_collection(collection_name)
            #load text from url
            text = requests.get(url).text
            #split text into chunks
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            #add chunks to collection
            for i, chunk in enumerate(chunks):
                collection.add(documents=[chunk], ids=[str(i)])
        except Exception as e:
            client.delete_collection(collection_name)
            raise HTTPException(status_code=500, detail="Error creating collection")
    
    results = collection.query(
        query_texts=[query],
        n_results=num_of_results
    )
    
    return results["documents"][0]


