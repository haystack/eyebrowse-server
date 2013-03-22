SIGNATURE = "- The Eyebrowse Team"

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
	'subject': 'Feedback for commerical production',
	'content': """
		'Feedback received from: %s <br><br> %s'
	"""
}