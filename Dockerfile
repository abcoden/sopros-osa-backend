FROM python:3.11.6-alpine3.18

RUN \
  echo "install shadow" && \
  apk add --no-cache --update shadow && \
  echo "add appuser with homedir and group" && \
  useradd -m -d /home/appuser -U -u 1001 appuser && \
  echo "uninstall shadow" && \
  apk del -r shadow && \
  # pip upgrade increases the image by 20MB
  #echo "update pip" && \
  #pip --no-cache install --upgrade pip && \
  #pip cache purge && \
  echo "baseimage with user created"

COPY dist/sopros_osa_backend-0.0.1.tar.gz /tmp/pip_app.tar.gz

RUN \
  pip install /tmp/pip_app.tar.gz && \
  rm -f /tmp/pip_app.tar.gz

USER 1001

CMD ["uvicorn", "sopros_osa_backend.main:app"]



  

