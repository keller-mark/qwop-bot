# Slime Soccer Bot

### Setup
- docker

```
docker build -t "slime-bot" .
docker run -v bot:/bot -d --name slime_bot slime-bot
docker exec -it slime_bot sh
# to exit: exit
docker stop slime_bot
docker rm slime_bot
```
