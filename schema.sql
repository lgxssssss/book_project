create table if not exists users(
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(50) not null unique,
    password varchar(50) not null
);
create table if not exists books(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `book_name` varchar(100) not null,
    `title_image` varchar(200),
    `price` double
);
create table if not exists order(
    oid INTEGER PRIMARY KEY AUTOINCREMENT,
    uid varchar(100) not null,
    id varchar(200) not null,
    `price` double
);

ALTER TABLE books ADD book_desc varchar(200);

alter table orders drop column u_name 