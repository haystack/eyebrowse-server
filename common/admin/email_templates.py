SIGNATURE = "- the Eyebrowse team"

alt_email = {
    'subject': 'Confirm your alternate email',
    'content': """
                Hi %s,
                <br>
                <br>
                Please confirm that you are the owner of
                 %s by clicking <a href='%s'>here</a>.
                 If you did not initiate this, ignore this.
                <br>
                <br>
                """ + SIGNATURE
}


feedback = {
    'subject': 'Feedback for Eyebrowse',
    'content': """ 'Feedback received from: %s \n\n %s' """
}

follow_email = {
    'subject': "%s is now following you on Eyebrowse!",
    'content': """
        Hi %s,
        \n
        \n
        %s is now following you on http://eyebrowse.csail.mit.edu!
        Check out their profile: %s.
        And here you can see all the people that are following you: %s.
        \n
        \n
        """ + SIGNATURE
}
