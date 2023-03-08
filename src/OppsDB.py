import mysql.connector

class Database:

	def OppsDB():
		# Connect to the database
		cnx = mysql.connector.connect(
			host="localhost",
			user="root",
			password="xojva1-nukjit-piWtaj",
			database="grant_opportunities"
		)

		# Create a cursor
		cursor = cnx.cursor()

		#Create Database
		#cursor.execute("CREATE DATABASE GrantOpps")

		# Define the dictionary
		# Define the query
		query = 'INSERT INTO grant_opps (Opp_id) VALUES (%(Opp_id)s)'

		# Execute the query
		cursor.execute(query, data)

		# Commit the changes
		cnx.commit()

		# Close the connection
		cnx.close()



