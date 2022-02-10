DROP TABLE IF EXISTS posts;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS healthcheck;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users (id)
);

CREATE TABLE healthcheck (id SERIAL PRIMARY KEY, datetime TIMESTAMP);
