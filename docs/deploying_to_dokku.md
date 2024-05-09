# Deploying to Dokku

## Prepare plugins

Ensure that the [Postgres plugin](https://github.com/dokku/dokku-postgres) is installed

```bash
# On your Dokku host:
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
```

## Create Dokku app

```bash
# On your Dokku host:

# Create a new app with the name dokku-demo
dokku apps:create dokku-demo
```

## Configure Postgres service

```bash
# On your Dokku host:

# Create a new Postgres service
dokku postgres:create dokku-demo-postgres

# Link the Postgres service to your Dokku app
dokku postgres:link dokku-demo-postgres dokku-demo
```

## Configure environment variables

```bash
# On your Dokku host:

# Generate and set SECRET_KEY
dokku config:set dokku-demo SECRET_KEY=$(python3 -c "import secrets; print(''.join(secrets.choice([chr(i) for i in range(0x21, 0x7F)]) for i in range(60)));")

# Set ALLOWED_HOSTS
dokku config:set dokku-demo ALLOWED_HOSTS=dokku-demo.example.com

# Set CSRF_TRUSTED_ORIGINS
dokku config:set dokku-demo CSRF_TRUSTED_ORIGINS=https://dokku-demo.example.com

# Set SENTRY_DSN
dokku config:set dokku-demo SENTRY_DSN=https://sentry-dsn-here.com/
```

## Configure Dokku to build and release the `production` Docker image stage

```bash
# On your Dokku host:

# Add "--target production" to the build args
dokku docker-options:add dokku-demo build "--target production"
```

## Configure git and push your app

```bash
# On your development machine:

git remote add dokku dokku@example.com:dokku-demo
git push dokku main
```

## Configure SSL/TLS

Assuming you have a `tar` file with your certificates

```bash
# On your Dokku host:

# Add your certificates to the app
dokku certs:add dokku-demo < /path/to/certs/dokku-demo.example.com.tar
```

## Configure networking

```bash
# On your Dokku host:

# Forward requests from host ports 80 and 443 to container port 8000
dokku proxy:ports-set dokku-demo http:80:8000 https:443:8000
```
