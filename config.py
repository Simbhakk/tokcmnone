import os



DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://devilbot:Rajbot@cluster0.ldrbggy.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Publicsave2")
