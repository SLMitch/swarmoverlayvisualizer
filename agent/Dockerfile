FROM docker:stable
RUN apk add --update \
    python \
    py-pip \
  && pip install requests \
  && rm -rf /var/cache/apk/*

COPY *py /app/
ENTRYPOINT [""]

CMD python /app/agent.py
