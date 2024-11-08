# How to deploy?

### Docker Dev Environment

[nginx.conf](./docs/nginx.conf) contains the nginx configurations

Use [docker-compose.yml](./docs/docker-compose.yml) for running the application

```bash
sudo docker compose up -d
sudo docker compose logs -f
```