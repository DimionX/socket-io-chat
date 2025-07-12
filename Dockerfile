FROM python:3.12-slim AS builder

WORKDIR /workspace

COPY requirements.txt package.json package-lock.json ./
COPY src/static src/static

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
      curl \
      python3-dev \
      gnupg \
      ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    rm -rf /var/lib/apt/lists/* && \
    npm ci && \
    npm run build && \
    pip wheel --no-cache-dir -w /wheels -r requirements.txt

FROM python:3.12-slim
WORKDIR /workspace

COPY --from=builder /wheels /wheels
COPY requirements.txt .

RUN apt-get update  \
    && apt-get install -y curl  \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --no-index \
      --find-links /wheels \
      -r requirements.txt && \
    rm -rf /wheels

COPY src .
COPY --from=builder /workspace/src/public/assets /workspace/public/assets

RUN useradd -m user && chown -R user:user /workspace \
    && mkdir -p /home/user/secrets \
    && chown -R user:user /home/user/secrets

USER user

ENV TOTP_USED_PATH="/home/user/secrets/totp_used"
