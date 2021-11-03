FROM ubuntu:focal as base

ARG UID=1000

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV TZ UTC

ENV SERVER_NAME localhost
ENV CONVERSION_HOST convertit
ENV CAPTURE_HOST screamshotter
ENV POSTGRES_HOST postgres
ENV PGPORT 5432

RUN mkdir -p /opt/georiviere-admin/var

RUN useradd -ms /bin/bash django --uid ${UID}
RUN chown -R django:django /opt

COPY .docker/update.sh /usr/local/bin/update.sh
COPY .docker/entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

WORKDIR /opt/georiviere-admin
VOLUME /opt/georiviere-admin/var

RUN apt-get update -qq && apt-get install -y -qq \
    python3.9 \
    gettext \
    # geodjango \
    binutils \
    gdal-bin \
    libproj-dev \
    # manage \
    netcat \
    tzdata \
    # mapentity
    iproute2 \
    # weasyprint
    fonts-liberation \
    libcairo2 \
    libfreetype6 \
    libgdk-pixbuf2.0 \
    libpango1.0-0 \
    libpangocairo-1.0-0 \
    libpq5 &&\
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

FROM base as build

ARG REQUIREMENTS=requirements.txt

RUN apt-get update -qq && apt-get install -y -qq \
    git \
    python3.9-dev \
    python3.9-venv \
    build-essential \
    libffi-dev \
    libfreetype6-dev \
    libgdk-pixbuf2.0-dev \
    libssl-dev \
    libpq-dev \
    libxml2-dev \
    libxslt-dev && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

USER django

RUN python3.9 -m venv /opt/venv
RUN  /opt/venv/bin/pip install --no-cache-dir pip setuptools wheel -U
COPY ${REQUIREMENTS} /opt/requirements.txt

# geotrek setup fix : it required django before being installed... TODO: fix it in geotrek setup.py
RUN  /opt/venv/bin/pip install --no-cache-dir django==2.2.*
RUN  /opt/venv/bin/pip install --no-cache-dir -r /opt/requirements.txt

FROM base as prod

ENV GUNICORN_CMD_ARGS "--workers 1 --timeout 3600 --bind 0.0.0.0:8000 --timeout 3600"

RUN apt-get update -qq && \
    apt-get full-upgrade && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

COPY --chown=django:django --from=build /opt/venv /opt/venv
COPY --chown=django:django georiviere /opt/georiviere-admin/georiviere
COPY --chown=django:django manage.py /opt/georiviere-admin/manage.py

RUN SECRET_KEY=temp-secret-key /opt/venv/bin/python ./manage.py compilemessages

CMD ["gunicorn", "georiviere.wsgi:application"]
