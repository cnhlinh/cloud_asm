# LinhCNH Final Test - Basic Cloud

FastAPI app with S3 file upload and AWS RDS PostgreSQL connection, containerised with Docker and deployed to EC2 via GitHub Actions.

## Features

- `POST /upload` — upload a file to S3
- `GET /health` — health check endpoint
- RDS PostgreSQL connection via `db.py`

## Requirements

- Python 3.12+
- Docker & Docker Compose
- AWS account with an S3 bucket and RDS PostgreSQL instance

## Environment Variables

Create a `.env` file in the project root:

```env
RDS_HOST=your-instance.xxxx.us-east-1.rds.amazonaws.com
DB_NAME=your_db
DB_USER=your_db_user
DB_PASSWORD=your_password
S3_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1

# Local only — leave unset on EC2 to use the attached IAM role
AWS_PROFILE=LinhCNH
```

## Run Locally

```bash
uv run uvicorn main:app --reload
```

Test the RDS connection:

```bash
uv run python db.py
```

## Run with Docker

```bash
docker compose up --build -d
```

## Deploy to EC2

### First-time setup on EC2

```bash
# Copy project files
scp -i your-key.pem -r /path/to/LinhCNH_FinalTest_BasicCloud ec2-user@<EC2_IP>:~/cloud_asm

# SSH in
ssh -i your-key.pem ec2-user@<EC2_IP>

# Create .env on the instance
cd ~/cloud_asm
nano .env

# Build and start
sudo docker compose up --build -d
```

### CI/CD via GitHub Actions

Every push to `main` automatically SSHes into EC2, pulls the latest code, and restarts the container.

Add these secrets in **GitHub → Settings → Secrets and variables → Actions**:

| Secret | Value |
|---|---|
| `EC2_HOST` | EC2 public IPv4 address |
| `EC2_USERNAME` | `ec2-user` (Amazon Linux) or `ubuntu` |
| `EC2_SSH_KEY` | Contents of your `.pem` file |
