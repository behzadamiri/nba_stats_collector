from decouple import config

# Database configuration
DB_TYPE = config("DB_TYPE", default="sqlite")  # SQLite as default database
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME", default="nba_stats.db")  # SQLite database file name
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")

# Build the connection string
if DB_TYPE == "sqlite":
    DATABASE_URL = f"{DB_TYPE}:///{DB_NAME}"
else:
    DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Other settings
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
