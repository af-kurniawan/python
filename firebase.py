import firebase_admin
from firebase_admin import firestore
import json

test_json = {
	"Book1":
	{
		"Title": "The Fellowship of the Ring",
		"Author": "J.R.R. Tolkien",
		"Genre": "Epic fantasy",
		"Price": 100
	},
	"Book2":
	{
		"Title": "The Two Towers",
		"Author": "J.R.R. Tolkien",
		"Genre": "Epic fantasy",
		"Price": 100	
	},
	"Book3":
	{
		"Title": "The Return of the King",
		"Author": "J.R.R. Tolkien",
		"Genre": "Epic fantasy",
		"Price": 100
	},
	"Book4":
	{
		"Title": "Brida",
		"Author": "Paulo Coelho",
		"Genre": "Fiction",
		"Price": 100
	}
}

def connect_db():
	global db

	cred = firebase_admin.credentials.Certificate('creds/re-project-e68e3-firebase-adminsdk-p4lhr-c2e053a223.json')
	firebase_admin.initialize_app(cred)
	db = firestore.client()

def add_json(file_path):
	with open(file_path, 'r') as f:
		data = json.load(f)

	# ref = db.reference("/")
	keys = data.keys()
	for key in keys:
		doc_ref = db.collection(u'listings').document(key)
		doc_ref.set(data[key])
		

connect_db()
add_json('data.json')
# print('test')