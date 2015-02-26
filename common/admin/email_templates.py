SIGNATURE = "- the Eyebrowse team"

alt_email = {
	'subject': 'Confirm your alternate email',
	'content': """
		Hi %s,
		<br>
		<br>
		Please confirm that you are the owner of  %s by clicking <a href='%s'>here</a>. If you did not initiate this, ignore this.
		<br>
		<br>
	""" + SIGNATURE
}


feedback = {
	'subject': 'Feedback for Eyebrowse',
	'content': """
		'Feedback received from: %s <br><br> %s'
	"""
}

follow_email = {
	'subject': "%s is now following you on Eyebrowse!",
	'content': """
		Hi %s,
		<br>
		<br>
		%s is now following you on <a href='http://eyebrowse.csail.mit.edu'>Eyebrowse</a>! 
		Check out their profile <a href="%s">here</a>. 
		And you can check out all the people that are following you <a href="%s">here</a>.
		<br>
		<br>
		""" + SIGNATURE
			
}