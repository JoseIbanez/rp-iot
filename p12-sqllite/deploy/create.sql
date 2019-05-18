
drop table reading;

CREATE TABLE reading (
   sensorId  text,
   nameId    text,
   value     number,
   datetime  datetime,
   PRIMARY KEY (sensorId, nameId, datetime)
);

CREATE TABLE sensor_hits (
   sensorId  text,
   counter     number,
   PRIMARY KEY (sensorId)
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


INSERT INTO sensor_hits(sensorId, counter) 
SELECT "ESP001", 0
WHERE NOT EXISTS(SELECT 1 FROM sensor_hits WHERE sensorId = "ESP001");

UPDATE sensor_hits
SET counter = counter+1
WHERE sensorId = "ESP001";