Teach
=====

Teach is a Django app for organizing courses, lecures
and their content.

Quick start
-----------

1. install the app using pip:
 	
 	either clone the repo and install from the directory of `setup.py`

	```
	git clone https://github.com/endremborza/riki-teach.git
	pip install riki-teach/
	```
	
	or simply install from github:
	
	`pip install git+https://github.com/endremborza/riki-teach.git`

2. Add "teach" to your INSTALLED_APPS setting like this:

	```python
    INSTALLED_APPS = [
        ...
        'teach',
    ]
	```
3. Include the teach URLconf in your project urls.py like this::

	```python
    path('teach/', include('teach.urls')),
	```
4. Run `python manage.py makemigrations` to create db migrations.

5. Run `python manage.py migrate` to create the teach models.

6. Start the development server with `python manage.py runserver` and visit http://127.0.0.1:8000/teach/testcreate/logic this will create a test-course to look at.

7. Visit http://127.0.0.1:8000/teach/ to look at it.

