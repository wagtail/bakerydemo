# Replace gunicorn's 'Server' HTTP header to avoid leaking info to attackers
import gunicorn

gunicorn.SERVER_SOFTWARE = ""
