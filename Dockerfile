FROM makinacorpus/geodjango:bionic-3.6

ARG UID=1000

ENV SERVER_NAME localhost
ENV CONVERSION_HOST convertit
ENV CAPTURE_HOST screamshotter
ENV POSTGRES_HOST postgres
ENV PGPORT 5432
ENV CACHE 00

RUN apt-get update -qq && apt-get install -y -qq \
    # manage \
    netcat \
    # mapentity
    iproute2 \
    # weasyprint
    fonts-liberation \
    libcairo2 \
    libffi-dev  \
    libfreetype6-dev \
    libgdk-pixbuf2.0-dev \
    libpango1.0-0 \
    libpangocairo-1.0-0 \
    libssl-dev \
    libxml2-dev \
    libxslt-dev && \
    apt-get install -y --no-install-recommends postgis && \
    apt-get -y -qq full-upgrade && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

RUN mkdir -p /code/public/media /code/public/static /code/private/cache

RUN useradd -ms /bin/bash django --uid ${UID}
RUN chown -R django:django /code

USER django

RUN python3.6 -m venv /code/venv
RUN  /code/venv/bin/pip install --no-cache-dir pip setuptools wheel -U
COPY requirements.txt /code/requirements.txt
# geotrek setup fix : it required django before being installed... TODO: fix it in geotrek setup.py
RUN  /code/venv/bin/pip install --no-cache-dir django==2.2.*
RUN  /code/venv/bin/pip install --no-cache-dir -r /code/requirements.txt

COPY .docker/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY --chown=django:django src /code/src

WORKDIR /code/src
VOLUME /code/public

ENTRYPOINT ["entrypoint.sh"]

CMD ["gunicorn", "georiviere.wsgi:application", "--workers", "1", "--timeout", "3600", "--bind", "0.0.0.0:8000", "--timeout", "3600"]
