# Local installation:

Install curl
```bash
sudo apt install curl
```

Install nvm
```bash
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.bashrc
```

Now we should install npm and node. This versions.
```bash
  "engines" : {
    "npm" : "9.3.1",
    "node" : "v19.2.0"
  }
```

Install npm and node
```bash
nvm install 19.2.0
npm install -g npm@9.3.1
```

Check versions
```bash
npm -v
node -v
```

# Local Usage:
Just use 'make run' in ./egmont directory after venv installation (poetry install)
Go to localhost:8000

# Container Usage:
Use 'make up' in base directory in first terminal to run django
```bash
make up
```
Use 'make vue-watch' in base directory to run vue server
```bash
make vue-install  # install dependencies
make vue-watch  # run dev server + build static + watch static
```
Go to localhost:8000

## Env:

For local/container development use env:
```bash
DJANGO_VITE_DEV_MODE=True
```

For dev/prod deploy use:
```bash
DJANGO_VITE_DEV_MODE=False
```
