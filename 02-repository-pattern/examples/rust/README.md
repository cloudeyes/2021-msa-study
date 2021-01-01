# Repository Pattern Example for Rust

- Author: Joseph Kim \<cloudeyes@gmail.com\>

## Prerequisitives

### Install Rust

(TODO) Link to the guide document


### Install required system libraries

- CentsOS / RHEL
  ```
  $ sudo yum install sqlite-devel postgresql-devel
  ```
- Ubuntu
  ```
  $ sudo apt install libsqlite3-dev libpq-dev
  ```

### Project setup

Using "[Diesel](https://diesel.rs/)" ORM library for Rust.

Please refer to the official document:
- [Diesel: Getting started](https://diesel.rs/guides/getting-started/)

**Notable differences to the official document**
- `.env` : `DATABASE_URL=app.db`

### Test

**Using [cargo-watch](https://crates.io/crates/cargo-watch)**

- `cargo install cargo-watch`
- `cargo watch -x test`
