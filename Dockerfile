FROM ubuntu:focal as base

ARG UID=1000
ARG REQUIREMENTS=requirements.txt

ENV DEBIAN_FRONTEND noninteractive
ENV SERVER_NAME localhost
ENV CONVERSION_HOST convertit
ENV CAPTURE_HOST screamshotter
ENV POSTGRES_HOST postgres
ENV PGPORT 5432
ENV CACHE 00

RUN mkdir -p /opt/georiviere-admin/public/media /opt/georiviere-admin/public/static /opt/georiviere-admin/private/cache

RUN useradd -ms /bin/bash django --uid ${UID}
RUN chown -R django:django /opt

COPY .docker/entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

WORKDIR /opt/georiviere-admin
VOLUME /opt/georiviere-admin/public

RUN apt-get update -qq && apt-get install -y -qq \
    python3.8 \
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

RUN apt-get update -qq && apt-get install -y -qq \
    git \
    python3.8-dev \
    python3.8-venv \
    build-essential \
    libffi-dev  \
    libfreetype6-dev \
    libgdk-pixbuf2.0-dev \
    libssl-dev \
    libpq-dev \
    libxml2-dev \
    libxslt-dev && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

USER django

RUN python3.8 -m venv /opt/venv
RUN  /opt/venv/bin/pip install --no-cache-dir pip setuptools wheel -U
COPY ${REQUIREMENTS} /code/requirements.txt
# geotrek setup fix : it required django before being installed... TODO: fix it in geotrek setup.py
RUN  /opt/venv/bin/pip install --no-cache-dir django==2.2.*
RUN  /opt/venv/bin/pip install --no-cache-dir -r /code/requirements.txt

FROM base as prod

ENV GUNICORN_CMD_ARGS "--workers 1 --timeout 3600 --bind 0.0.0.0:8000 --timeout 3600"

RUN apt-get update -qq && \
    apt-get full-upgrade && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

COPY --chown=django:django --from=build /opt/venv /opt/venv
COPY --chown=django:django georiviere /opt/georiviere-admin/georiviere
COPY --chown=django:django manage.py /opt/georiviere-admin/manage.py

CMD ["gunicorn", "georiviere.wsgi:application"]
