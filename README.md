# **Messanger / Django** </br>

### Deploy project on your local machine </br>

1 - To deploy project on your local machine create new virtual environment and execute this command:<br />

`pip install -r requirements.txt`<br />

2 - Migrate db models to SQLite3:<br />

`./manage.py migrate`</br>

3 - Manage superuser:</br>

`./manage.py createsuperuser` <br />
`./manage.py changepassword` <br />

4 - Run app:<br />

`./manage.py runserver`<br />

5 - For authorization with Token add to HEADERS method:<br />

"Authorization": "JWT your-token-id"<br />

6 - API:<br />

`/api/v1/threads/?page=1` - pagination <br />

`/api/v1/threads/` - GET threads list, POST thread <br />
`/api/v1/threads/<pk>/` - GET, PUT, DELETE thread <br />

`/api/v1/threads/<pk>/messages/` - GET messages list for the thread, POST message for the thread <br />
`/api/v1/threads/<pk>/messages/read/` - SET messages read=True if False <br />
`/api/v1/messages/<pk>/` - GET, PUT, DELETE the message <br />

./manage.py dumpdata dialogs.thread --format=json --indent=4 > threads.json
