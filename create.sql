create table base (
    datetime text primary key,
    num char(9) not null,
    crop char(30),
    image char(30),
    res text,
    cam_name char(30)
);
