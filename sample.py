from flask import flask, url_for

from app import students

#HTML -Hardcoded HTML content
'<a href=" ' + url_for('students') + '">students,</a>'

#Right way - url_for
'<a href=" ' + url_for('students') + '">View Students</a>'

#url_for('students') will generate the URL for the 'students' route defined in app,py en
