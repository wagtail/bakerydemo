# Wagtail demo project

This is a demonstration project for the amazing [Wagtail CMS](https://github.com/wagtail/wagtail).

The demo site is designed to provide examples of common features and recipes to introduce you to Wagtail development. Beyond the code, it will also let you explore the admin / editorial interface of the CMS.

Note we do _not_ recommend using this project to start your own site - the demo is intended to be a springboard to get you started. Feel free to copy code from the demo into your own project.

### Wagtail Features Demonstrated in This Demo

This demo is aimed primarily at developers wanting to learn more about the internals of Wagtail, and assumes you'll be reading its source code. After browsing the features, pay special attention to code we've used for:

- Dividing a project up into multiple apps
- Custom content models and "contexts" in the "breads" and "locations" apps
- A typical weblog in the "blog" app
- Example of using a "base" app to contain misc additional functionality (e.g. Contact Form, About, etc.)
- "StandardPage" model using mixins borrowed from other apps
- Example of customizing the Wagtail Admin via _wagtail_hooks_
- Example of using the Wagtail "snippets" system to represent bread categories, countries and ingredients
- Example of a custom "Galleries" feature that pulls in images used in other content types in the system
- Example of creating ManyToMany relationships via the Ingredients feature on BreadPage
- Lots more

**Document contents**

- [Installation](#installation)
- [Next steps](#next-steps)
- [Contributing](#contributing)
- [Other notes](#other-notes)

# Installation

- [Gitpod](#setup-with-gitpod)
- [Vagrant](#setup-with-vagrant)
- [Docker](#setup-with-docker)
- [Virtualenv](#setup-with-virtualenv)

If you want to see what Wagtail is all about, we suggest trying it out through [Gitpod](#setup-with-gitpod).
If you want to set up Wagtail locally instead, and you're new to Python and/or Django, we suggest you run this project on a Virtual Machine using [Vagrant](#setup-with-vagrant) or [Docker](#setup-with-docker) (whichever you're most comfortable with). Both Vagrant and Docker will help resolve common software dependency issues.
Developers more familiar with virtualenv and traditional Django app setup instructions should skip to [Setup with virtualenv](#setup-with-virtualenv).

## Setup with Gitpod

Set up a development environment and run this demo website with a single click (requires a Github account):

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/wagtail/bakerydemo/)

Once Gitpod has fully started, and a preview of the bakery website has appeared in the "Simple Browser" panel, click the arrow button to the right of the URL bar to open the website in a new tab.
Go to `/admin/` and login with `admin / changeme`.

## Setup with Vagrant

#### Dependencies

- [Vagrant](https://www.vagrantup.com/)
- [Virtualbox](https://www.virtualbox.org/)

#### Installation

Once you've installed the necessary dependencies run the following commands:

```bash
git clone https://github.com/wagtail/bakerydemo.git
cd bakerydemo
vagrant up
vagrant ssh
# then, within the SSH session:
./manage.py runserver 0.0.0.0:8000
```

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/) and the Wagtail admin
interface at [http://localhost:8000/admin/](http://localhost:8000/admin/).

Log into the admin with the credentials `admin / changeme`.

Use `Ctrl+c` to stop the local server. To stop the Vagrant environment, run `exit` then `vagrant halt`.

## Setup with Docker

#### Dependencies

- [Docker](https://docs.docker.com/engine/installation/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

Run the following commands:

```bash
git clone https://github.com/wagtail/bakerydemo.git
cd bakerydemo
docker compose up --build -d
```

After this command completes and returns to the command prompt, wait 10 more seconds for the database setup to complete. Then run:

```bash
docker compose run app /venv/bin/python manage.py migrate
docker compose run app /venv/bin/python manage.py load_initial_data
```
If this fails with a database error, wait 10 more seconds and re-try. Finally, run:

```bash
docker compose up
```

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/) and the Wagtail admin
interface at [http://localhost:8000/admin/](http://localhost:8000/admin/).

Log into the admin with the credentials `admin / changeme`.

**Important:** This `docker-compose.yml` is configured for local testing only, and is _not_ intended for production use.

### Debugging

To tail the logs from the Docker containers in realtime, run:

```bash
docker compose logs -f
```

## Setup with Virtualenv

You can run the Wagtail demo locally without setting up Vagrant or Docker and simply use Virtualenv, which is the [recommended installation approach](https://docs.djangoproject.com/en/3.2/topics/install/#install-the-django-code) for Django itself.

#### Dependencies

- Python 3.7, 3.8, 3.9, 3.10 or 3.11
- [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
- [VirtualenvWrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) (optional)

### Installation

With [PIP](https://github.com/pypa/pip) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
installed, run:

    mkvirtualenv wagtailbakerydemo
    python --version

Confirm that this is showing a compatible version of Python 3.x. If not, and you have multiple versions of Python installed on your system, you may need to specify the appropriate version when creating the virtualenv:

    deactivate
    rmvirtualenv wagtailbakerydemo
    mkvirtualenv wagtailbakerydemo --python=python3.9
    python --version

Now we're ready to set up the bakery demo project itself:

    cd ~/dev [or your preferred dev directory]
    git clone https://github.com/wagtail/bakerydemo.git
    cd bakerydemo
    pip install -r requirements/development.txt

Next, we'll set up our local environment variables. We use [django-dotenv](https://github.com/jpadilla/django-dotenv)
to help with this. It reads environment variables located in a file name `.env` in the top level directory of the project. The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

    cp bakerydemo/settings/local.py.example bakerydemo/settings/local.py
    cp .env.example .env

To set up your database and load initial data, run the following commands:

    ./manage.py migrate
    ./manage.py load_initial_data
    ./manage.py runserver

Log into the admin with the credentials `admin / changeme`.

# Next steps

Hopefully after you've experimented with the demo you'll want to create your own site. To do that you'll want to run the `wagtail start` command in your environment of choice. You can find more information in the [getting started Wagtail CMS docs](https://docs.wagtail.org/en/stable/getting_started/index.html).

# Contributing

If you're a Python or Django developer, fork the repo and get stuck in! If you'd like to get involved you may find our [contributing guidelines](https://github.com/wagtail/bakerydemo/blob/master/contributing.md) a useful read.

### Preparing this archive for distribution

If you change content or images in this repo and need to prepare a new fixture file for export, do the following on a branch:

```bash
./manage.py dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.rendition -e sessions -e wagtailsearch.indexentry -e wagtailsearch.sqliteftsindexentry -e wagtailcore.referenceindex -e wagtailcore.pagesubscription > bakerydemo/base/fixtures/bakerydemo.json
prettier --write bakerydemo/base/fixtures/bakerydemo.json
```

Please optimize any included images to 1200px wide with JPEG compression at 60%. Note that `media/images` is ignored in the repo by `.gitignore` but `media/original_images` is not. Wagtail's local image "renditions" are excluded in the fixture recipe above.

Make a pull request to https://github.com/wagtail/bakerydemo

# Other notes

### Note on demo search

Because we can't (easily) use ElasticSearch for this demo, we use wagtail's native DB search.
However, native DB search can't search specific fields in our models on a generalized `Page` query.
So for demo purposes ONLY, we hard-code the model names we want to search into `search.views`, which is
not ideal. In production, use ElasticSearch and a simplified search query, per
[https://docs.wagtail.org/en/stable/topics/search/searching.html](https://docs.wagtail.org/en/stable/topics/search/searching.html).

### Sending email from the contact form

The following setting in `base.py` and `production.py` ensures that live email is not sent by the demo contact form.

`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

In production on your own site, you'll need to change this to:

`EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`

and configure [SMTP settings](https://docs.djangoproject.com/en/3.2/topics/email/#smtp-backend) appropriate for your email provider.

### Testing Content-Security-Policy compliance in Wagtail

Bakerydemo is set up in such a way that it can be used to test [Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) compatibility in Wagtail. It uses [django-csp](https://django-csp.readthedocs.io/en/latest/index.html) to generate the appropriate [CSP HTTP header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy).

By default, `django-csp` is not enabled since Wagtail isn't fully compatible yet. Set the `CSP_DEFAULT_SRC` environment variable in your `.env` file to set the default policy. An example can be found in `.env.example`.

### Users included in demo data

The demo data includes users with different roles and preferences. You can use these users to quickly test the permission system in Wagtail or how localization is handled in the admin interface.

| Username    | Password   | Superuser | Groups     | Preferred language | Timezone      | Active |
| ----------- | ---------- | --------- | ---------- | ------------------ | ------------- | ------ |
| `admin`     | `changeme` | Yes       | None       | undefined          | undefined     | Yes    |
| `editor`    | `changeme` | No        | Editors    | undefined          | undefined     | Yes    |
| `moderator` | `changeme` | No        | Moderators | undefined          | undefined     | Yes    |
| `inactive`  | `changeme` | yes       | None       | undefined          | undefined     | No     |
| `german`    | `changeme` | yes       | None       | German             | Europe/Berlin | Yes    |
| `arabic`    | `changeme` | yes       | None       | Arabic             | Asia/Beirut   | Yes    |

### Ownership of demo content

All content in the demo is public domain. Textual content in this project is either sourced from Wikimedia (Wikipedia for blog posts, [Wikibooks for recipes](https://en.wikibooks.org/wiki/Cookbook:Table_of_Contents)) or is lorem ipsum. All images are from either Wikimedia Commons or other copyright-free sources.
