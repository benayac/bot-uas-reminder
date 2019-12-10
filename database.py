import pyrebase
from secrets import *

config = {
  "apiKey": database_api,
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "path/to/serviceAccountCredentials.json"
}
firebase = pyrebase.initialize_app(config)