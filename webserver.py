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
 
from database_setup import Restaurant, Base, MenuItem





##Stablish the link with DB
engine = create_engine('sqlite:///restaurantmenu.db')
##Create a session that is bind to the database "engine"
DBSession = sessionmaker(bind = engine)
#Stablish a session name as "session"
session = DBSession()
#Fetch all restaurants an store in a variable named restaurants

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
			##If entering to EDIT restaurant link
			if self.path.endswith("/edit"):
				#Get the id from the URL
				restaurantIDPath = self.path.split("/")[2]
				#Query the restaurant to get just the one with that id
				myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
				if myRestaurantQuery:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = "<html><body>"
					output += "<h1>"
					output += myRestaurantQuery.name
					output += "</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
					output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</form>"
					output += "</body></html>"
					self.wfile.write(output)

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
					##Return the id in the link for edit - Has to be converted to string
					output += "<a href= 'restaurants/%s/edit'>Edit</a>" % restaurant.id
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

			##Catch the post for EDIT
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'mulitpart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					restaurantIDPath = self.path.split("/")[2]

					myRestaurantQuery = session.query(Restaurant).filter_by(
						id=restaurantIDPath).one()
					if myRestaurantQuery != []:
						myRestaurantQuery.name = messagecontent[0]
						session.add(myRestaurantQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

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
