FROM python:3.10.7-slim-bullseye

RUN adduser --disabled-password --gecos '' e_commerce_user

USER e_commerce_user
WORKDIR /home/e_commerce_user/app

ENV PATH="/home/e_commerce_user/.local/bin:$PATH"
COPY --chown=e_commerce_user:e_commerce_user requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY --chown=e_commerce_user:e_commerce_user . .

CMD [ "sh", "run.sh" ]
