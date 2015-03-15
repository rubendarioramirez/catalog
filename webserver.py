import cgi
import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

##Import SQLALCHEMY Libs to use CRUD
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
##Stablish the link with DB
engine = create_engine('sqlite:///restaurantmenu.db')
##Create a session that is bind to the database "engine"
DBSession = sessionmaker(bind = engine)
#Stablish a session name as "session"
session = DBSession()
#Fetch all restaurants an store in a variable named restaurants

 ##Creating restaurant class to be able to interactve with it
class Restaurant(Base):
    __tablename__ = 'restaurant'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 

class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>&#161 Hola !</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			##When /restaurant is acceded.
			if self.path.endswith("/restaurant"):
				restaurants = session.query(Restaurant).all()						
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				#Make a new restaurant link
				output += "<a href=/restaurant/new>Add a new restaurant</a>"
				#Iterates through the restaurants and print 1 name per h1. Can also use LI to make it more elegant
				for restaurant in restaurants: 
					output += "<h1>" + restaurant.name + "</h1>"
					output += "<a href=#>Delete</a>"
					output += "<br>"
					output += "<a href=#>Edit</a>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			##If entering to Add new restaurant link
			if self.path.endswith("/restaurant/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>&#161 Add a new restaurant !</h1>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><h2>Restaurant name</h2><input name="newRestaurantName" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		try:
			if self.path.endswith("/restaurant/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('newRestaurantName')

				#Create the new name in the database
				newRestaurant = Restaurant(name = messagecontent[0])
				session.add(newRestaurant)
				session.commit()
			
				##Close the headers and redirect to homepage
				self.send_response(301)
				self.send_header('content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()
			
				#ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				#if ctype == 'multipart/form-data':
				#	fields=cgi.parse_multipart(self.rfile, pdict)
				#	messagecontent = fields.get('message')
				#output = ""
				#output +=  "<html><body>"
				#output += " <h2> Okay, how about this: </h2>"
				#output += "<h1> %s </h1>" % messagecontent[0]
				#output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				#output += "</html></body>"
				#self.wfile.write(output)
				#print output
		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s"  % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()

engine = create_engine('sqlite:///restaurantmenu.db')
 
Base.metadata.create_all(engine)
