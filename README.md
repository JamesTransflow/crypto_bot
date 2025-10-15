## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation and Running

1. Navigate to the project root directory:
```bash
cd crypto_bot
```

2. config `OPENAI_API_KEY` environment varialbe
```bash
export OPENAI_API_KEY="sk-..."
```

2. Build and start the application:
```bash
docker compose up -d --build
```

3. Open your browser and visit:
```
http://localhost:3000/
```

### Management Commands

Stop the application:
```bash
docker compose down
```

View backend logs:
```bash
docker logs -f crypto_bot_backend
```
