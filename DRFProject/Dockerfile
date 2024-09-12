FROM python:3.12-alpine
WORKDIR /DRFProject

RUN apk add postgresql-dev
COPY --from=app requirements.txt .
RUN pip install -r requirements.txt && pip install supervisor

COPY supervisord.conf /etc/supervisord.conf
COPY --from=app . .

ENTRYPOINT supervisord -c /etc/supervisord.conf

EXPOSE 8000