FROM python:3.11-slim-bullseye

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static
RUN mkdir -p $PYTHONPATH/media

# where the code lives
WORKDIR $PYTHONPATH

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl \
  # translations
  gettext \
  # uuid generator
  uuid-runtime \
  # ffmpeg
  ffmpeg

# install dependencies
RUN pip install --upgrade pip
RUN pip install setuptools

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# install python dependencies
COPY pyproject.toml poetry.lock ./
# export poetry to requirements.txt, only main dependencies
RUN poetry export -f requirements.txt --without-hashes --only main -o requirements.txt
# install python dependencies
RUN pip install -r requirements.txt
# remove requirements.txt
RUN rm requirements.txt

# copy entrypoint.sh
COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# install app
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/entrypoint"]
