# auto-oglasi

* pip
* bower
* MySQL

### Create DB
> Create MySQL database and import `database.sql`


### Virtual environment
```
$ source venv/bin/activate
```

### Configure Flask application
> Copy `app/settings-example.cfg` to `app/settings.cfg` and configure
```
$ export AUTOOGLASI_SETTINGS=settings.cfg
```

### Installing requiraments
```
$ pip install -r requirements.txt
$ bower install
```

### Run
```
$ python run.py
open http://localhost:5000/
```

Default credentials:
admin@admin.com:admin123