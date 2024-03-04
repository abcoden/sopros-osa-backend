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

COPY dist/sopros_osa_backend-${VERSION}.tar.gz /tmp/pip_app.tar.gz

# pip cache is saved at /var/tmp/buildah-cache-1000/root/.cache/pip/
# see https://github.com/containers/podman/discussions/15612
RUN \
  --mount=type=cache,target=/root/.cache pip install /tmp/pip_app.tar.gz && \
  rm -f /tmp/pip_app.tar.gz

USER 1001

EXPOSE 8000

ENTRYPOINT ["uvicorn", "sopros_osa_backend.main:app", "--port=8000", "--host=0.0.0.0"]



  

