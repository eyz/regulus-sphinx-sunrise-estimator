FROM python:3-slim

# Regulus-Sphinx prophecy alignment optimizer.
# Contains both models; select at runtime via argument:
#
#   docker run regulus-sphinx single       # single-moment model (default)
#   docker run regulus-sphinx sequential   # sequential morning-arc model
#
# Bake DE441 into the image to skip first-run download:
#   docker build --build-arg INCLUDE_EPHEMERIS=1 -t regulus-sphinx-full .

ARG INCLUDE_EPHEMERIS=0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY regulus_upcoming_alignment.py .
COPY regulus_optuna_optimizer.py .
COPY regulus_optuna_optimizer_sequential.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN mkdir -p /app/data

# Conditionally download DE441 during build using Skyfield's own downloader.
# DE441 (JPL Development Ephemeris 441) provides high-precision Sun positions
# needed for dawn scoring. Source: Park et al. (2021), AJ 161, 105
RUN if [ "$INCLUDE_EPHEMERIS" = "1" ]; then \
      echo "Downloading DE441 ephemeris (~3.1 GB) into image..." && \
      python3 -c "\
from skyfield.api import load; \
load.directory = '/app/data'; \
load('de441.bsp')"; \
    fi

VOLUME /app/data

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
CMD ["single"]
