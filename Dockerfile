FROM ubuntu:focal as base
# stage with general requirements
ARG UID=1000

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV TZ UTC

ENV SERVER_NAME localhost
ENV CONVERSION_HOST convertit
ENV CAPTURE_HOST screamshotter
ENV POSTGRES_HOST postgres
ENV POSTGRES_PORT 5432
ENV CUSTOM_SETTINGS_FILE /opt/georiviere-admin/var/conf/custom.py

RUN mkdir -p /opt/georiviere-admin/var

RUN useradd -ms /bin/bash django --uid ${UID}
RUN chown -R django:django /opt

COPY .docker/update.sh /usr/local/bin/update.sh
COPY .docker/entrypoint.sh /usr/local/bin/entrypoint.sh

WORKDIR /opt/georiviere-admin

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
    libpq5 && \
    apt-get install -y -qq --no-install-recommends postgis && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

USER django
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 8000

FROM base as build
# stage with build requirements
USER root

RUN apt-get update -qq && apt-get install -y -qq \
    git \
    python3.9-dev \
    python3.9-venv \
    build-essential \
    graphviz \
    libffi-dev \
    libfreetype6-dev \
    libgdk-pixbuf2.0-dev \
    libssl-dev \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libgraphviz-dev \
    pkg-config && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

USER django

RUN python3.9 -m venv /opt/venv
RUN  /opt/venv/bin/pip install --no-cache-dir pip setuptools wheel -U
# geotrek setup fix : it required django before being installed... TODO: fix it in geotrek setup.py
RUN  /opt/venv/bin/pip install --no-cache-dir django==2.2.*

COPY requirements.txt /opt/requirements.txt
RUN  /opt/venv/bin/pip install --no-cache-dir -r /opt/requirements.txt

FROM build as dev
# stage with dev requirements
COPY dev-requirements.txt /opt/dev-requirements.txt
RUN  /opt/venv/bin/pip install --no-cache-dir -r /opt/dev-requirements.txt

CMD ./manage.py runserver 0.0.0.0:8000

FROM base as prod
# stage with prod requirements only
ENV GUNICORN_CMD_ARGS "--workers 1 --timeout 3600 --bind 0.0.0.0:8000 --timeout 3600"

USER root

RUN apt-get update -qq && \
    apt-get full-upgrade -y -qq && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

COPY --chown=django:django --from=build /opt/venv /opt/venv
COPY --chown=django:django georiviere /opt/georiviere-admin/georiviere
COPY --chown=django:django manage.py /opt/georiviere-admin/manage.py

USER django

RUN SECRET_KEY=temp-secret-key /opt/venv/bin/python ./manage.py compilemessages

CMD ["gunicorn", "georiviere.wsgi:application"]
