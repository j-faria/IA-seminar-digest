# IAporto-seminar-digest

### Steps 

- Create the event in google calendar

	In the title of the event put  
	  (S) Title  
	  (CS) Title  
	depending if it is a Seminar or a Cookie Seminar

	In the location field put  
	Auditorium  
	1st floor classroom

	Remember to add it to the 'IA-UPORTO-seminars' calendar !

	In the description put  
	Name of presenter (affiliation) (new line)  
	Abstract

- Save the event
- Run `python create_email_html.py` and enter the dates for the seminars of that week. 
- If you use Thunderbird:  
	- Open the html file created by `create_email_html.py` (with a text editor, not a browser!)
	- Copy everything (Ctrl-A then Ctrl-C)
	- Create a new email in Thunderbird.
	- In the body click Insert > HTML
	- Paste the HTML code (Ctrl-V)
	- Click Insert
	- Fill the email addresses and you're ready to send the email!

- If you use Gmail
	- Open the html file created by `create_email_html.py` (with a browser!!)
	- Copy everything (Ctrl-A then Ctrl-C)
	- Compose a new email in Gmail
	- Paste everything in the body (Ctrl-V)
	- Fill the email addresses and you're ready to send the email!

You're done!

