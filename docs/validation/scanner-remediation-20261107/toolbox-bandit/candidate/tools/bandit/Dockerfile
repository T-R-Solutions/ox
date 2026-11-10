ARG BASE
FROM ${BASE}
ARG SNAPSHOT
RUN test -n "$SNAPSHOT" \
    && rm -f /etc/apt/sources.list.d/debian.sources \
    && printf 'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/%s/ trixie main\n' "$SNAPSHOT" > /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends ca-certificates python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
COPY payload /payload/
RUN python3 -m venv /opt/bandit \
    && /opt/bandit/bin/pip install --no-index --no-deps --require-hashes --find-links=/payload -r /payload/requirements.txt \
    && /opt/bandit/bin/pip check \
    && mkdir /toolbox && printf '[bandit]\n' > /toolbox/bandit.ini \
    && dpkg-query -W > /toolbox/packages.tsv \
    && /opt/bandit/bin/pip list --format=json > /toolbox/python-packages.json \
    && python3 --version > /toolbox/python-version.txt
ENV PATH="/opt/bandit/bin:$PATH" PYTHONDONTWRITEBYTECODE=1
WORKDIR /src
ENTRYPOINT ["bandit"]
