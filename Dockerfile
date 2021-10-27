FROM makinacorpus/geodjango:bionic-3.6

ENV SERVER_NAME localhost
ENV CONVERSION_HOST convertit
ENV CAPTURE_HOST screamshotter
ENV CACHE 00

RUN apt-get update -qq && apt-get install -y -qq \
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
    libxslt-dev \
    libffi-dev && \
    apt-get install -y --no-install-recommends postgis && \
    apt-get -y -qq full-upgrade && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt/*

RUN mkdir -p /code/src /code/public/media /code/public/static /code/private/cache

RUN useradd -ms /bin/bash django
RUN chown -R django:django /code

USER django

RUN python3.6 -m venv /code/venv
RUN  /code/venv/bin/pip install --no-cache-dir pip setuptools wheel -U

COPY .docker/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY src /code/src
WORKDIR /code/src
VOLUME /code/public

RUN /code/venv/bin/pip3 install --no-cache-dir django>=2.2
RUN /code/venv/bin/pip3 install --no-cache-dir -r requirements.txt -U

ENTRYPOINT ["entrypoint.sh"]

CMD ["gunicorn", "georiviere.wsgi:application", "--workers", "1", "--timeout", "3600", "--bind", "0.0.0.0:8000", "--timeout", "3600"]
