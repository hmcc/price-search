create table asda_price_scrape
(
  id serial primary key,
  product_code integer not null,
  title varchar(200) not null,
  size varchar(50),
  price_pence integer not null,
  unit varchar(50),
  unit_price_pence integer
);
