#!/bin/bash

PROJECT_NAME=$1

: ${PROJECT_DIR:=/vagrant}
: ${DEV_USER:=vagrant}
VIRTUALENV_DIR=/home/$DEV_USER/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


# Virtualenv setup for project
su - $DEV_USER -c "virtualenv --python=python3 $VIRTUALENV_DIR"
# Replace previous line with this if you are using Python 2
# su - $DEV_USER -c "virtualenv --python=python2 $VIRTUALENV_DIR"

su - $DEV_USER -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"


# Upgrade PIP
su - $DEV_USER -c "$PIP install --upgrade pip"

# Install PIP requirements
su - $DEV_USER -c "$PIP install -r $PROJECT_DIR/requirements/base.txt"


# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# copy local settings file
cp $PROJECT_DIR/bakerydemo/settings/local.py.example $PROJECT_DIR/bakerydemo/settings/local.py
# add .env file for django-dotenv environment variable definitions
echo DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.local > $PROJECT_DIR/.env

if [ -n "$USE_POSTGRESQL" ]
then
    su - $DEV_USER -c "createdb $PROJECT_NAME"
    su - $DEV_USER -c "$PIP install \"psycopg2-binary>=2.7,<3\""
    cat << EOF >> $PROJECT_DIR/bakerydemo/settings/local.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$PROJECT_NAME',
    }
}
EOF
fi

# Run syncdb/migrate/load_initial_data/update_index
su - $DEV_USER -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput && \
                   $PYTHON $PROJECT_DIR/manage.py load_initial_data && \
                   $PYTHON $PROJECT_DIR/manage.py update_index"


# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/$DEV_USER/.bashrc
export PYTHONPATH=$PROJECT_DIR

alias dj="./manage.py"
alias djrun="dj runserver 0.0.0.0:8000"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF
