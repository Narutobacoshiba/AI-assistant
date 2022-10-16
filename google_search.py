try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
  
def search(query): 

    for p in search(query, tld="co.in", num=1, stop=100, pause=2):
        return p 