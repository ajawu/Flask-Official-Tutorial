# Flaskr Blog

A Blog created with Flask, SQLAlchemy, and Pydantic. Features include:-

- Posts
    - Create, update and delete post with CKEditor support (Login Required)
    - View posts by author or category
    - View post author
- Comments
    - Add comment to existing post
- User
    - Register
    - Login
    - Change Password
    - Change profile information

## Sample Page
1. Home Page.

    ![Home](/flaskr-sample-image.png)

## Installation

Use the package manager [poetry](https://python-poetry.org/) to install Flaskr dependencies.
1. Clone the repository

   ```bash
   git clone git@github.com:ajawu/Flask-Official-Tutorial.git
   ```
2. Cd into project directory and setup project with poetry

   ```bash
   cd Flask-Official-Tutorial/
   poetry install
   ```

## Usage

```bash
export FLASK_APP=flaskr

export FLASK_ENV=development
flask init-db
flask run
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](/LICENSE)
