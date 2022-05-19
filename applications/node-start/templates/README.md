# {{{project_name}}}
## dev ops
### npm
Given that we are using `npm`, make sure:
1. you have it installed, and
2. you run `npm ci` whenever `package-lock.json` changes, including right after cloning the repo.

### do.py
`do.py` is a runnable listing of dev ops. `./do.py --help` for help. `python3` is required.

## glossary

## API
### auth
#### `POST /auth/signup`
body:
```
{
    email: <email>,
    password: <password>,
}
```

#### `POST /auth/login`
body:
```
{
    email: <email>,
    password: <password>,
}
```

#### `POST /auth/logout`

### hello
#### `GET /hello/world`
successful response: `'Hello, world!'`

### controls
#### `POST /admin/control/:id`
body:
```
{
    value,
}
```
