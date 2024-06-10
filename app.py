import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
<center> 
    <h1>Welcome to Save restricted website </h1>
    <h3> Hi , If you are able to see this website ,</br> then it means our bot is working perfectly</h3>
    <img src="https://graph.org/file/121de3eeefcb047facd3e.jpg" style="border-radius: 12px;"/>
    <br><br><br>
    <h1>Our channel lists</h1>
    <h2>1. Save Restricted content :- <a href="https://telegram.me/RajZ_bots">Click here </a></h2>
    <h2>2. Save Restricted Message:- <a href="https://telegram.me/Save_Restricted_content">Click here</a></h2>
    <br>
    <h1>Our Bot lists</h1>
    <h2>1. Save Restricted Message :- <a href="https://t.me/Save_Restricted_contentx_Bot">click here</a></h2>
    <h2>2. Save Restricted content:- <a href="https://telegram.me/Save_Restricted_Content_Raj_Bot">click here</a></h2>
    
</center> 
<style>
    body { 
        background: antiquewhite;
    }
</style>"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
