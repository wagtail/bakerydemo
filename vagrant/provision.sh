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
su - $DEV_USER -c "cd $PROJECT_DIR && $PIP install -r requirements/base.txt"


# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# copy local settings file
cp $PROJECT_DIR/bakerydemo/settings/local.py.example $PROJECT_DIR/bakerydemo/settings/local.py
# add .env file for django-dotenv environment variable definitions
echo DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings.local > $PROJECT_DIR/.env

if [ -n "$USE_POSTGRESQL" ]
then
    echo Creating database.....
    DB_EXISTS=$(
        su - $DEV_USER -c \
        "psql -lqt | cut -d \| -f 1 | grep -q '^ $PROJECT_NAME $' && echo yes || echo no"
    )
    if [[ "$DB_EXISTS" == "no" ]]; then
        echo Database does not exist, creating...
        su - $DEV_USER -c "createdb $PROJECT_NAME"
    else
        echo Database already exists, skipping...
    fi
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

BASHRC="/home/$DEV_USER/.bashrc"

# Just put these values BASHRC_LINE_* to .bashrc:
BASHRC_LINE_1="export PYTHONPATH=$PROJECT_DIR"
BASHRC_LINE_2="alias dj='$PROJECT_DIR/manage.py'"
BASHRC_LINE_3="alias djrun='dj runserver 0.0.0.0:8000'"
BASHRC_LINE_4="export PS1='[$PROJECT_NAME \W]\\$ '"
BASHRC_LINE_5="cd $PROJECT_DIR"
BASHRC_LINE_ACTIVATE="source $VIRTUALENV_DIR/bin/activate"

NEEDS_UPDATE_BASHRC_ACTIVATE=no

# Prevent duplicate values in .bashrc from repeat provision
# "seq 1 2" is used just in case: if the number of lines will increase
for i in $(seq 1 5);
do
    eval "CURRENT_LINE=\$BASHRC_LINE_$i"
    LINE_EXISTS=$(cat $BASHRC | grep -q "^$CURRENT_LINE" && echo yes || echo no)
    if [[ "$LINE_EXISTS" == "no" ]];
    then
        echo $CURRENT_LINE >> $BASHRC
        NEEDS_UPDATE_BASHRC_ACTIVATE=yes
    fi
done

# Prevent a situation when "source" had called before env vars were provided
if [[ "$NEEDS_UPDATE_BASHRC_ACTIVATE" == "yes" ]];
then
	cat $BASHRC | grep -v "^$BASHRC_LINE_ACTIVATE" > "${BASHRC}.tmp" && mv ${BASHRC}.tmp $BASHRC
	echo $BASHRC_LINE_ACTIVATE >> $BASHRC
fi
