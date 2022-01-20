From python:3.7

WORKDIR qna

ENV AWSCLI_VERSION=2.2.1

RUN set -x \
    && apt-get update && apt-get install -y curl git nano make cmake curl unzip \
    && apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/{apt.dpkg,cache,log}

COPY src/pkg/requirements.txt ./pkg/requirements.txt 

RUN set -x \
    && pip install -U pip \
    && pip install -r ./pkg/requirements.txt \
    && python -m nltk.downloader universal_tagset \
    && python -m nltk.downloader stopwords \
    && python -m spacy download en

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

RUN wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz \
    && tar -xvf s2v_reddit_2015_md.tar.gz

COPY src/pkg ./pkg

CMD python3 ./pkg/main.py