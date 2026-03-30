# Wagtail demo project

This is a demonstration project for the amazing [Wagtail CMS](https://github.com/wagtail/wagtail).

The demo site is designed to provide examples of common features and recipes to introduce you to Wagtail development. Beyond the code, it will also let you explore the admin/editorial interface of the CMS.

Note that we do _not_ recommend using this project to start your own site - the demo is intended to be a springboard to get you started. Feel free to copy code from the demo into your own project.

### Wagtail Features Demonstrated in This Demo

This demo is aimed primarily at developers wanting to learn more about the internals of Wagtail, and assumes you'll be reading its source code. After browsing the features, pay special attention to code we've used for:

- Dividing a project up into multiple apps
- Custom content models and "contexts" in the "breads" and "locations" apps
- A typical weblog in the "blog" app
- Example of using a "base" app to contain miscellaneous functionality (e.g. Contact Form, About, etc.)
- "StandardPage" model using mixins borrowed from other apps
- Example of customizing the Wagtail Admin via _wagtail_hooks_
- Example of using the Wagtail "snippets" system to represent bread categories, countries, and ingredients
- Example of a custom "Galleries" feature that pulls in images used in other content types in the system
- Example of creating ManyToMany relationships via the Ingredients feature on BreadPage
- And much more

**Document contents**

- [Installation](#installation)
- [Next steps](#next-steps)
- [Contributing](#contributing)
- [Other notes](#other-notes)

# Installation

- [Venv](#setup-with-venv)
- [Vagrant](#setup-with-vagrant)
- [Docker](#setup-with-docker)

If you want to see what Wagtail is all about, we suggest trying it out locally in a virtual environment. See [Setup with venv](#setup-with-venv).

If you're new to Python and/or Django, we suggest you run this project on a virtual machine using [Docker](#setup-with-docker) or [Vagrant](#setup-with-vagrant) (whichever you're most comfortable with). Both Vagrant and Docker will help resolve common software dependency issues.

## Setup with Vagrant

#### Dependencies

- [Vagrant](https://www.vagrantup.com/)
- [Virtualbox](https://www.virtualbox.org/)

#### Installation

Once you've installed the necessary dependencies, run the following commands:

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
git clone https://github.com/wagtail/bakerydemo.git --config core.autocrlf=input
cd bakerydemo
docker compose up --build -d
```

After this command completes and returns to the command prompt, wait 10 more seconds for the database setup to complete. Then run:

```bash
docker compose exec app /venv/bin/python manage.py migrate
docker compose exec app /venv/bin/python manage.py load_initial_data
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

To tail the logs from the Docker containers in real time, run:

```bash
docker compose logs -f
```

## Setup with venv

You can run the Wagtail demo locally without setting up Vagrant or Docker and simply use venv, which is the [recommended installation approach](https://docs.djangoproject.com/en/5.2/topics/install/#install-the-django-code) for Django itself.

#### Dependencies

- Python 3.10+
- [venv](https://docs.python.org/3/library/venv.html)

### Installation

On GNU/Linux or macOS (bash):

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, activate the virtual environment using the appropriate command for your shell:

```bash
# PowerShell
.venv\Scripts\Activate.ps1
# Command Prompt (cmd.exe)
.venv\Scripts\activate.bat
```
> **Note (PowerShell Execution Policy)**
> If activating with `Activate.ps1` fails with an error like “running scripts is disabled on this system”, you can either:
> - use `.venv\Scripts\activate.bat` in Command Prompt, or
> - allow scripts in PowerShell for your user account:
>   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Now we're ready to set up the bakery demo project itself:
```bash
cd ~/dev [or your preferred dev directory]
git clone https://github.com/wagtail/bakerydemo.git
cd bakerydemo
pip install -r requirements/development.txt
```

Next, we need to create the files `.env` and `bakerydemo/settings/local.py`, which provide a place for local configuration settings that need to be kept outside of version control. No such settings are required for a standard installation, but warnings will be displayed if these files are not present:
```bash
cp bakerydemo/settings/local.py.example bakerydemo/settings/local.py
cp .env.example .env
# `cp` is used for bash. Windows Command Prompt uses `copy`
```

To set up your database and load initial data, run the following commands:
```bash
./manage.py migrate
./manage.py load_initial_data
./manage.py runserver
```

Log into the admin with the credentials `admin / changeme`.

# Next steps

After experimenting with the demo, you may want to create your own site. To do that, run the `wagtail start` command in your environment of choice. You can find more information in the [getting started Wagtail CMS docs](https://docs.wagtail.org/en/stable/getting_started/index.html).

# Contributing

Check out our [contributing documentation](contributing.md) for our contributing guidelines and docs for common tasks.

# Other notes

### Local configuration files

The `bakerydemo/settings/local.py` file can be used to store local Django settings such as database connection details that need to be kept outside of version control.

Additionally, various settings can be controlled through environment variables. The [python-dotenv](https://github.com/theskumar/python-dotenv) package is used to load these variables from a `.env` file in the project root.

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

and configure [SMTP settings](https://docs.djangoproject.com/en/stable/topics/email/#smtp-backend) appropriate for your email provider.

### Users included in demo data

The demo data includes users with different roles and preferences. You can use these users to quickly test the permission system in Wagtail or how localization is handled in the admin interface.

| Username    | Password   | Superuser | Groups     | Preferred language | Timezone      | Active |
| ----------- | ---------- | --------- | ---------- | ------------------ | ------------- | ------ |
| `admin`     | `changeme` | Yes       | None       | undefined          | undefined     | Yes    |
| `editor`    | `changeme` | No        | Editors    | undefined          | undefined     | Yes    |
| `moderator` | `changeme` | No        | Moderators | undefined          | undefined     | Yes    |
| `inactive`  | `changeme` | Yes       | None       | undefined          | undefined     | No     |
| `german`    | `changeme` | Yes       | None       | German             | Europe/Berlin | Yes    |
| `arabic`    | `changeme` | Yes       | None       | Arabic             | Asia/Beirut   | Yes    |

### Ownership of demo content

All content in the demo is public domain. Textual content in this project is either sourced from Wikimedia (Wikipedia for blog posts, [Wikibooks for recipes](https://en.wikibooks.org/wiki/Cookbook:Table_of_Contents)) or consists of lorem ipsum text. All images are from either Wikimedia Commons or other copyright-free sources.
