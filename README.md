# Hello!

We've put together a minimal [Django](https://docs.djangoproject.com) project
to get you started. The aim of this task is to focus on the requirements and
code so we hope this helps keep that clear.

# Setup

Please use *Python 3* (for completeness, we used `3.7.2` at the time of writing).
Then:

```bash
pip install -r requirements.txt

./manage.py migrate
./manage.py createsuperuser --username root --email root@getcoconut.local
./manage.py runserver
```

You should now be able to view the webserver:

* http://localhost:8000/api/ - The API root
* http://localhost:8000/admin/ - The Django Admin

# Work

You should use the `./acme/current_account` module to do your work in. Commit as you
would normally. At the end you'll need to package up your repository to send back.
Don't worry too much about the commit history itself, we're most interested in 
the finished code.

# Tests

We have created a few placeholders for tests that we expect to run at minimum.

You should be able to run the tests within `acme/current_account/test.py` as follows
(this is from the root directory of the project). Before any changes you should
get 3 failures:

```bash
pytest
```

# Submitting

You should export this project back to a `git bundle` when complete and then
email both the bundle and database file as a single zip. Do this from the 
root of the project folder (i.e where this `README` file is located). Please
name the zip file with your initials then `.backend.zip`, eg `ac.backend.zip`:

```bash
git bundle create acme-complete.bundle --all
zip -9 initials.backend.zip acme.bundle db.sqlite3
```

If you have any problems creating a bundle just `zip` up the whole cloned folder
(that is, the project root where this `README` exists).

