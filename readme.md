Wagtail demo project
=======================

This is a demonstration project for [Wagtail CMS](http://wagtail.io).

*We do __not__ recommend using this project to start your own site*. This project is only to provide some examples of
implementing common features, it is not an exemplar of Django or Wagtail best practice.

If you're reasonably new to Python/Django, we suggest you run this project on a Virtual Machine using Vagrant, which
helps  resolve common software dependency issues. However for more experienced developers, instructions to start this
project without Vagrant follow below.

Once you're familiar with the examples in this project and you want to start a real site, we strongly recommend running
the ``wagtail start`` command in a fresh virtual environment, explained in the
[Wagtail CMS Documentation](http://wagtail.readthedocs.org/en/latest/getting_started/).

Setup with Vagrant
------------------

### Dependencies
* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant 1.5+](http://www.vagrantup.com)

### Installation
Run the following commands:

```bash
git clone git@github.com:wagtail/bakerydemo.git
cd wagtaildemo
vagrant up
vagrant ssh
# then, within the SSH session:
./manage.py runserver 0.0.0.0:8000
```

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/) and the Wagtail admin
interface at [http://localhost:8000/admin/](http://localhost:8000/admin/).

Log into the admin with the credentials ``admin / changeme``.

Setup without Vagrant
-----
Don't want to set up a whole VM to try out Wagtail? No problem.

### Dependencies
* [PIP](https://github.com/pypa/pip)

### Installation

With PIP installed run the following commands:

    git clone git@github.com:wagtail/bakerydemo.git
    cd wagtaildemo
    pip install -r requirements.txt

Next, we'll set up our local environment variables. We use [django-dotenv](https://github.com/jpadilla/django-dotenv)
to help with this. It reads environment variables located in a file name .env in the top level directory of the project. The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

    $ cp bakerydemo/settings/local.py.example bakerydemo/settings/local.py
    $ echo "DJANGO_SETTINGS_MODULE=bakerydemo.settings.local" > .env

Execute the following commands:

    ./manage.py migrate
    ./manage.py load_initial_data
    ./manage.py runserver

Log into the admin with the credentials ``admin / changeme``.

### Note on demo search:

Because we can't (easily) use ElasticSearch for this demo, we use wagtail's native DB search.
However, native DB search can't search specific fields in our models on a generalized `Page` query.
So for demo purposes ONLY, we hard-code the model names we want to search into `search.views`, which is
not ideal. In production, use ElasticSearch and a simplified search query, per
[http://docs.wagtail.io/en/v1.8.1/topics/search/searching.html](http://docs.wagtail.io/en/v1.8.1/topics/search/searching.html).

### Heroku deployment:

If you need to deploy your demo site to a publicly accessible server [Heroku](https://heroku.com)
provides a one-click deployment solution:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wagtail/bakerydemo)

If you do not have a Heroku account, clicking the above button will walk you through the steps
to generate one.  After which, you will be presented with a screen to configure your app. For our purposes,
we will accept all of the defaults and click `Deploy`.  The status of the deployment will dynamically
update in the browser. Once finished, click `View` to see the public site.

Log into the admin with the credentials ``admin / changeme``.

To learn more about Heroku, read [Deploying Python and Django Apps on Heroku](https://devcenter.heroku.com/articles/deploying-python).

### Storing Wagtail Media Files on AWS S3

If you have deployed the demo site to Heroku, you may want to perform some additional setup.  Heroku uses an
[ephemeral filesystem](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem).  In laymen's terms, this means
that uploaded images will disappear at a minimum of once per day, and on each application deployment.  To mitigate this,
you can host your media on S3.

This documentation assumes that you have an AWS account, an IAM user, and a properly configured S3 bucket. These topics
are outside of the scope of this documentation; the following [blog post](https://wagtail.io/blog/amazon-s3-for-media-files/)
will walk you through those steps.

Next, you will need to add `django-storages` and `boto3` to `requirements/heroku.txt`.

Then you will need to edit `settings/heroku.py`:

    INSTALLED_APPS.append('storages')

You will also need to add the S3 bucket and access credentials for the IAM user that you created.

    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'changeme')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'changeme')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'changeme')
    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

Next, you will need to set these values in the Heroku environment.  The next steps assume that you have
the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed and configured. You will
execute the following commands to set the aforementioned environment variables:

    heroku config:set AWS_STORAGE_BUCKET_NAME=changeme
    heroku config:set AWS_ACCESS_KEY_ID=changeme
    heroku config:set AWS_SECRET_ACCESS_KEY=changeme

Do not forget to replace the `changeme` with the actual values for your AWS account.

Finally, we need to configure the `MEDIA_URL` as well as inform Django that we want to use `boto3` for the storage
backend:

    MEDIA_URL = 'https://{}/'.format(AWS_S3_CUSTOM_DOMAIN)'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

Commit these changes and push to Heroku and you should now have persistent media storage!

### Sending email from the contact form

The following setting in `base.py` and `heroku.py` ensures that live email is not sent by the demo contact form.

`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

In production on your own site, you'll need to change this to:

`EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`

and configure [SMTP settings](https://docs.djangoproject.com/en/1.10/topics/email/#smtp-backend) appropriate for your email provider.
