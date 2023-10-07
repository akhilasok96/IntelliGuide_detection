from gps import getCurrentLocation
import firebase_admin
databaseURL = 'https://intelliguide-29a3c-default-rtdb.asia-southeast1.firebasedatabase.app/'
cred_obj = firebase_admin.credentials.Certificate('./google.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	
	'databaseURL':databaseURL
	})
from firebase_admin import db
def upLoadLocation():
	lat,lng=getCurrentLocation()
	ref = db.reference("/location")
	ref.push().set({
		"latitude":lat,
		"longitde":lng
	})
upLoadLocation()
