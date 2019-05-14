
drop table reading;

CREATE TABLE reading (
   sensorId  text,
   nameId    text,
   value     number,
   datetime  datetime,
   PRIMARY KEY (sensorId, nameId, datetime)
);


/////////////////

insert into reading
   (sensorId, nameId, value, datetime)
values
   ("ESP33333", "Temp", 20.1, "2019-03-09 10:10");

/////////////////

insert or ignore into reading
   (sensorId, nameId, value, datetime)
values
   ("ESP33333", "Temp", 20.1, "2019-03-09 10:10");

