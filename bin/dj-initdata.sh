#!/usr/bin/env sh

# migrate databases
bin/dj.sh makemigrations
bin/dj.sh migrate

# load data
bin/dj.sh load_initial_data
