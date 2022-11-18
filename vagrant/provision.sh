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
su - $DEV_USER -c "cd $PROJECT_DIR && $PIP install -r requirements/development.txt"

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# Run syncdb/migrate/load_initial_data/update_index
su - $DEV_USER -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput && $PYTHON $PROJECT_DIR/manage.py load_initial_data"

# Add a couple of aliases to manage.py into .bashrc

BASHRC=/home/$DEV_USER/.bashrc
BASHRC_BACKUP="${BASHRC}__pre_provision_backup"

if [[ ! -f "$BASHRC_BACKUP" ]];
then
    # On the first provision run:
    # Create backup of .bashrc if it doesn't exist
    cp -f $BASHRC $BASHRC_BACKUP
else
    # If provision runs twice or more
    # restore "pure" .bashrc from the backup
    cp -f $BASHRC_BACKUP $BASHRC
fi


cat << EOF >> /home/$DEV_USER/.bashrc
export PYTHONPATH=$PROJECT_DIR

alias dj="$PROJECT_DIR/manage.py"
alias djrun="dj runserver 0.0.0.0:8000"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF
