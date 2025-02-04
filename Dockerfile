FROM  python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install selenium redis beautifulsoup4 requests undetected-chromedriver

RUN apt update && apt install git jq -y
RUN mkdir /app
WORKDIR /app
COPY .ssh /root/.ssh

RUN echo 42833
RUN chmod -R 600 /root/.ssh/ && git clone --depth 1 git@github.com:hofarah/site-crawler.git /app/site-crawler --branch master
ENTRYPOINT ["python"]

CMD ["/app/site-crawler/main_crawler.py"]
