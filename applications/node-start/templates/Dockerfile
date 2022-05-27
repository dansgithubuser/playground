FROM node:{{{node_image_tag}}}

WORKDIR /{{{project_name}}}

COPY package.json .
COPY package-lock.json .

RUN apt update
RUN apt install -y vim ripgrep
RUN npm ci

COPY config config
COPY migrations migrations
COPY src src
COPY do.py .
COPY git-state.txt .

EXPOSE 443
EXPOSE 80

ENTRYPOINT npm run start
