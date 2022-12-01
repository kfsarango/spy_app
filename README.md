# Spy App

Django app for manage spy data.

Stack:

- Django Framework
- PostgreSQL


### 👉 Set Up for `Unix`, `MacOS`

> 1. Set up `.env` file to set environments vars, use `.env.sample` as template.

> 2. Install dependencies.  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> 3. Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 4. Load Initial Data

```bash
$ python manage.py load_initial_data_hits
```
<br />

> 5. Start Application

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`.

Can Log In using this credentials:

| Email | Password | Type     |
|------|----------|----------|
|    giuseppi@gmail.com  |     passbigboss     | Big Boss |
|   jalley@gmail.com   |      passjalley    | Manager  |
|   sforney@gmail.com   |     passsforney     | Manager  |
|   mlogsdon@gmail.com   |     passmlogsdon     | Manager  |
|   hlomax@gmail.com   |     passhlomax     | Hitmen   |
|   kmcfadden@gmail.com   |     passkmcfadden     | Hitmen   |
|   aschaefer@gmail.com   |     passaschaefer     |    Hitmen      |
|   lback@gmail.com   |    passlback      |     Hitmen     |
|  pbronson@gmail.com    |      passpbronson    |    Hitmen      |
|   placksin@gmail.com   |     passplacksin     |    Hitmen      |
|   dlima@gmail.com   |     passdlima     |     Hitmen     |
|   ckeys@gmail.com   |     passckeys     |    Hitmen      |
|   amayfield@gmail.com   |     passamayfield     |    Hitmen      |


<br />
# spy_app
