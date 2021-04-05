# Μια ηλεκτρονική βιβλιοθήκη γραμμένη με Python 3 Flask
# και τεχνολογίες διαδικτύου HTML5, CSS3, Bootstrap 3, JavaScript, JQuery
# Δημιουργία: Νίκος-Νικήτας | Created by: Nikos-Nikitas
#--------------------------------------------------------------------------------------
#	Μια προσπάθεια για Full Stack Development.
#	-----------------------------------------------------------------------------------
#	An attempt for a full-stack developed e-library.
#	-----------------------------------------------------------------------------------
#	Αφήνω αυτόν τον κώδικα μαζί με τους άλλους ως εισφορά στον ανοικτό κώδικα.
#	-----------------------------------------------------------------------------------
#	Μπορείτε να τα χρησιμοποιήσετε αρκεί να με αναφέρετε για την αρχική μου προσπάθεια.
#	You may use this and other works of mine. Just mention me for my original attempt.
#	-----------------------------------------------------------------------------------
#	Πριν το χρησιμοποιήσετε, διαγράψτε το "books.db" 
#	και ξαναφτιάξτε τη βάση όπως τη θέλετε με το make_db.py
#	Before use delete the "books.db" and make your database
#	as you want it with make_db.py
#--------------------------------------------------------------------------------------
# 				- - - > Server Side < - - -

#Οι βιβλιοθήκες που θα χρησιμοποιήσουμε
from flask import Flask, render_template, request, url_for, redirect
import sqlite3 as sql #Η βιβλιοθήκη της βάσης δεδομένων
from contextlib import closing #Για να κλείνουμε τη βάση δεδομένων

#Ξεκινάμε την εφαρμογή
app = Flask(__name__)

#	Η κλάση Book περιλαμβάνει τα βιβλία με τίτλο και συγγραφέα.
#	Η συνάρτηση Add() προσθέτει τα βιβλία και τους συγγραφείς 
#	στις αντίστοιχες λίστες. Μετά δημιουργούμε αντικείμενα βιβλία
#	και τα προσθέτουμε από τη φόρμα index.html.
#	Τα βιβλία προστίθενται στη λίστα και μόνιμα στη βάση δεδομένων.
#	Η βάση δεδομένων φτιάχτηκε με το αρχείο make_db.py
#	και όποτε θέλουμε τη διαβάζουμε με το read_db.py
#	Και τα δυο scripts μου θα τα βρείτε μαζί στο αποθετήριό μου εδώ.
#	Η μεταβλητή numBooks δείχνει στο index.html τον αριθμό των βιβλίων. 
#	Για περισσότερα θα με βρείτε στο GitHub: nikosnikitas

class Book:
	
	def __init__(self,title,author):
		
		self.title = title
		self.author = author


#Δρομολογούμε στη σελίδα μιας και είναι εφαρμογή μιας σελίδας.
#Προσθέτει στη βάση δεδομένων εκτός κι αν υπάρχει κάποιο σφάλμα.
#Διαβάζει τις γραμμές της βάσης και στέλνει τα δεδομένα στον πίνακα της σελίδας
@app.route("/")
def index():
	try:
		with closing(sql.connect("books.db")) as c:
			with closing(c.cursor()) as cr:
				book_data = cr.execute("SELECT TITLE FROM BOOKS;").fetchall()
				books = [book[0] for book in book_data]
				numBooks = len(books)
				author_data = cr.execute("SELECT AUTHOR FROM BOOKS;").fetchall()
				authors = [author[0] for author in author_data]
				c.commit()
	except ValueError: #διαχείριση σφάλματος αν δοθεί κάτι μη έγκυρο
		return "<h1> Error in value. </h1>"
	finally:
		return render_template("index.html",numBooks=numBooks,books=books,authors=authors)

#	// Μπορεί να γίνει και προσθήκη ενός συστήματος ασφαλείας,
#	// εισαγωγής, ταυτοποίησης, σύνδεσης χρηστών
#	// και κρυπτογράφησης κωδικών.
#	-- Στην παρούσα φάση μπορεί να χρησιμοποιηθεί και για δοκιμές ασφαλείας --
#--------------------------------------------------------------------------------------

#	Δέχεται μόνο με μέθοδο "POST" τη φόρμα για ασφάλεια.
#	Παίρνει τα στοιχεία της φόρμας αν δεν είναι κενή, ανοίγει τη βάση δεδομένων,
#	και προσθέτει τα στοιχεία: τίτλο του βιβλίου και συγγραφέα
#	στον πίνακα BOOKS της βάσης books.db και επιστρέφει στην index()
#	για να μην αλλάζει η σελίδα
@app.route("/Add",methods=["POST"])
def Add():
	if request.method == "POST":
		res = request.form.get("myform")
		t = request.form.get("title")
		a = request.form.get("author")
		if t is not None:
			with closing(sql.connect("books.db")) as c:
				with closing(c.cursor()) as cr:
					cr.execute("INSERT INTO BOOKS (TITLE, AUTHOR) VALUES (?,?);",[t,a])
					c.commit()
					return index()

#	Αναζητεί στη βάση δεδομένων για ο,τι ψάξει ο χρήστης (βιβλίο/συγγραφέα)
#	και επιστρέφει τα αποτελέσματα δείχνοντάς μας και τον αντίστοιχο συγγραφέα 
#	του βιβλίου ή βιβλίο του συγγραφέα
#	Αν θέλουμε όλα τα βιβλία γράφουμε 'all'.
@app.route("/Search", methods=["POST","GET"])
def Search():
	searchbar = request.form.get("search")
	if searchbar is not None:
		with closing(sql.connect("books.db")) as c:
			with closing(c.cursor()) as cr:
				search_query = cr.execute("SELECT TITLE, AUTHOR FROM BOOKS WHERE TITLE LIKE ? OR AUTHOR LIKE ?;",[searchbar,searchbar])
				all_r = cr.fetchall()
				if len(all_r) == 0 and searchbar == "all":
					cr.execute("SELECT * FROM BOOKS;")
					c.commit()
					all_r = cr.fetchall()
					return render_template("search.html",all_r=all_r)
			return render_template("search.html",all_r=all_r)
	return render_template("search.html")
	

#Τρέχουμε την εφαρμογή ιστού στον server
if __name__ == "__main__":
	app.debug = False
	app.run()
	
#-------------------------------------------------------------------------------------------------
# Για γνωστές δυσλειτουργιες δείτε στο τέλος του κώδικα. 
#							-
# For known bugs look at the bottom of the page.
#-------------------------------------------------------------------------------------------------
# 			- - - > ΣΧΟΛΙΑ - COMMENTS < - - -

#- - - > ΚΑΙ ΠΙΘΑΝΕΣ ΠΡΟΣΘΗΚΕΣ - AND POSSIBLE ADDITIONS < - - -

# Ίσως γίνει καλύτερο με SQLAlchemy αντί για sqlite3.

# Οι εντολές για τη βάση δεδομένων θα μπορούσαν να μπουν σε μια συνάρτηση
# για εξοικονόμηση χώρου και μεγαλύτερη ταχύτητα σε μια μεγαλύτερη εφαρμογή.

# Η διαχείριση/ταυτοποίηση χρηστών μπορεί να γίνει όπως και με τα βιβλία,
# με τη διαφορά ότι πρέπει να υπάρχει ξεχωριστή συνεδρία (session) για κάθε
# χρήστη και ένα σύστημα ασφαλείας με κρυπτογράφηση για τους κωδικούς.

# Μπορεί να προστεθεί και ένας πίνακας διαχειριστή (admin panel).

#	- - - > ΓΝΩΣΤΕΣ ΔΥΣΛΕΙΤΟΥΡΓΙΕΣ - KNOWN BUGS < - - -

# Αφού προσθέσετε μια τιμή μην κάνετε ανανέωση γιατί μπορεί να πάρει διπλή τιμή.
# Αν κάποιος από την κοινότητα θελήσει και μπορέσει να το διορθώσει είναι ευπρόσδεκτος.
#							- - - - - - - - - - - 
# There is a known bug: if you give a value and refresh the page it adds the value again.
# If anyone from the community wants and makes it to fix this they are welcome.
