FROM python:3.11.6-alpine3.18

RUN \
  echo "install shadow" && \
  apk --no-cache update && \
  apk add --no-cache shadow && \
  echo "add appuser with homedir and group" && \
  useradd -m -d /home/appuser -U -u 1001 appuser && \
  echo "uninstall shadow" && \
  apk del -r shadow && \
  echo "update pip" && \
  pip install --upgrade pip && \
  echo "baseimage with user"

COPY dist/sopros_osa_backend-0.0.1.tar.gz /tmp/pip_app.tar.gz

RUN \
  pip install /tmp/pip_app.tar.gz

USER 1001

CMD ["uvicorn", "sopros_osa_backend.main:app"]



  

