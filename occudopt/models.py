from occudopt import db
from mongoengine import ListField, StringField, ReferenceField
import datetime

class Image(db.Document):
	image_path = StringField()
	#the code below

class Message(db.Document):
	message_from = ReferenceField('User')
	message_to = ListField(ReferenceField('User'))
	message_body = StringField(max_length = 2000)
	#message_images = ListField(ReferenceField('Image'))
	
# is a separate collection right for relationships?  Or should they be embedded documents?  Same with messages.  

#Relationships get created, and referenced in the appropriate people.  If a relationship ends, it gets a stop_date and gets pulled out of the people. 
#a search of relationships where x = person can yield all their out-of-date relationships.

class Relationship(db.Document):
	adopted_by = ReferenceField('User')
	adopted = ReferenceField('User')
	start_date = db.DateTimeField()
	stop_date = db.DateTimeField()
	
class Vouch(db.Document):
	vouchee = ReferenceField('User')
	voucher = ReferenceField('User')
	date = db.DateTimeField()

class User(db.Document):
	email = db.EmailField(required = True)
	first_name = db.StringField(max_length = 50)
	last_name = db.StringField(max_length = 50) 
	password = db.StringField(max_length = 200)
	philosophy = db.StringField(max_length = 1000)
	tags = ListField(StringField(max_length=100))
	is_group = db.BooleanField()
	pictures = ListField(ReferenceField('Image'))
	profile_picture = ReferenceField('Image')
	messages = ListField(ReferenceField('Message'))
	authenticated = db.BooleanField()
	adopting = ListField(ReferenceField('Relationship'))
	adopted_by = ListField(ReferenceField('Relationship'))
	primary_city = ReferenceField('OccupyCity')
	
	#  V----< this may be unnecessary 
	def	authenticate(self, value):
		if value:
			self.authenticated = value
		else:
			return self.authenticated

	def	is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return self.email

class OccupyCity(db.Document):
	name = db.StringField(max_length = 50)
	location = db.GeoPointField()
	url = db. URLField
	

	
	
	