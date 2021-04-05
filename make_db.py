#	Πρόγραμμα δημιουργίας βάσης δεδομένων
#	Δημιουργία: Νίκος-Νικήτας
#----------------------------------------------------------------------------------------------------------------------
#	Program that creates a SQLite database
#	Created by Nikos-Nikitas

import sqlite3 #η βιβλιοθήκη της βάσης δεδομένων

c = sqlite3.connect("books.db") #Συνδεόμαστε και 
								#δημιουργούμε νέα βάση δεδομένων 
								#αφού δεν υπάρχει
print("Database opened!") 

#	Η βάση άνοιξε!

#	Φτιάχνουμε πίνακα για τους χρήστες με όνομα και κωδικό
#c.execute("CREATE TABLE USERS (ID INT NOT NULL UNIQUE, USERNAME VARCHAR(255) NOT NULL UNIQUE, PASSWORD TEXT NOT NULL)")

#	Φτιάχνουμε πίνακα για τα βιβλία με τίτλο και συγγραφέα.
c.execute("CREATE TABLE BOOKS (TITLE TEXT NOT NULL, AUTHOR VARCHAR(255))")

print("Created tables successfully!")

#	Αποσυνδεόμαστε
#	κλείνοντας τη σύνδεση και το αρχείο της βάσης δεδομένων.
c.close()
