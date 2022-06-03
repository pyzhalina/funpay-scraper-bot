import dotenv
import os


dotenv.load_dotenv(".env")
token=os.environ["token"]
id=os.environ["id"] #в файле .env поменяйте id телеграма на ваш собственный (можно узнать с помощью @getmyid_bot)