# Movie Watchlist API

A Simple REST API to manage a movie watchlist.
Built with FastAPI, SQLModel/SQLAlchemy, containerized with Docker, GitHub Actions workflow file to automate the build, test, and deployment process, and Terraform configuration to define the infrastructure for deploying the REST application to a IBM Cloud environment.

## Features

1. `POST/items` - create a Movie: `{ "title": "Interstellar", "year": 2014, "watched": false }`
2. `GET/items` - List Movies
               - filter: `GET /items?watched=false`
3. `GET/health` - Health check
4. OpenAPI document interface: `/docs#`

## Tech Stack

1. Python: FastAPI, SQLModel (SQLAlchemy), Uvicorn

2. DB: SQLite

3. Container: Docker (non-root user, slim base, multi-arch build)

4. CI/CD: GitHub Actions (tests + GHCR push + Terraform deploy with approval)

5. Infra: IBM Cloud Code Engine (serverless, scale-to-zero)

6. IaC: Terraform

## Local Development

### Cloning the repository

1. Open Terminal.
2. Change the current working directory to the location where you want the cloned directory.
3. Type git clone, and then paste the URL mentiond below.

```console
git clone https://github.com/2887ankit/movie-watchlist-API.git
```

### Create and activate a python environment:

```console
python3 -m venv .venv
source .venv/bin/activate
```

### Install the needed dependencies with:

```console
pip install -r requirements.txt
```

### Start the server with the following:

```console
uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080
```

### Try Calling:

1. Check API health:

```console
curl "http://localhost:8080/health"
```

2. Create a movie:

```console
curl -X POST "http://localhost:8080/items" \
     -H "Content-Type: application/json" \
     -d '{"title": "Interstellar", "year": 2014, "watched": false}'
```

3. Retrieve movies

```console
curl "http://localhost:8080/items"
```

4. Filter unwatched movies

```console
curl "http://localhost:8080/items?watched=false"
```

5. Swagger UI:

visit: http://localhost:8080/docs#/

## API documentation

Access [http://localhost:8080/docs](http://localhost:8080/docs). From there you'll see all endpoints and can test your API

## Tests

Run the test suite (uses a test SQLite DB):

```console
pytest -q
```

## Docker

### Build

```console
docker build -t movie-watchlist:latest .
```

### Run (with local DB persisted to `./data`)

```console
mkdir -p data
docker run -d \
  -p 8080:8080 \
  -v "$(pwd)/data:/app" \
  --name movie-api \
  movie-watchlist:latest
```

## CI/CD (GitHub Actions)

### CI (`.github/workflows/ci.yml`)

 - Installs Python dependencies

 - Runs `pytest`

 - Builds Docker image

 - Pushes image to GHCR: `ghcr.io/<owner>/movie-watchlist-api:latest` (`on main`)

Authentication uses the built-in `GITHUB_TOKEN` with `packages: write`.

### CD (`.github/workflows/cd.yml`)

 - Triggers after CI (`workflow_run`) or on manual `workflow_dispatch`

 - Runs Terraform `init/validate/plan/apply`

 - Requires manual approval via GitHub Environment `prod`

 - Prints a clickable App URL in the job summary

### Setup required in GitHub repo:

1. Repo -> Settings -> Secrets and variables -> Actions: add `IBMCLOUD_API_KEY`.

2. Repo -> Settings -> Environments: create `prod`, enable Required reviewers.

3. Push to `main` -> CI builds and pushes image -> CD waits for approval -> deploys.

## Deploy to IBM Cloud (Terraform)

Terraform code can be found in `movie-watchlist/terraform`.

### Prerequisite

- IBM Cloud account and API key

- Region matches variables (default `eu-gb`)

- Resource group name - `"Default"`

### Variables of note

- `image_reference` (required): e.g. `ghcr.io/<owner>/movie-watchlist-api:latest`

- `image_port`: default `8080`

- `scale_cpu_limit`: `"0.25"`, `scale_memory_limit`: `"0.5G"`

- `scale_min_instances`: `0` (scale-to-zero), `scale_max_instances`: `1`

- `database_url`: default SQLite

### Useful commands (for running on local)

```console
export IBMCLOUD_API_KEY=<YOUR-API-KEY>
cd terraform
terraform init
terraform plan -var "resource_group=Default" \
               -var "image_reference=ghcr.io/<owner>/movie-watchlist-api:latest"
terraform apply -auto-approve -var "resource_group=Default" \
                             -var "image_reference=ghcr.io/<owner>/movie-watchlist-api:latest"
terraform output -raw app_url
```