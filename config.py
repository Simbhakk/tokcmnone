import os



DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://foruse:amanbhai@cluster0.kgjebee.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Publicsave3")
