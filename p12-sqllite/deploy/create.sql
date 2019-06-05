
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


CREATE TABLE sensor_state (
   sensorId      text,
   alias         text,
   description   text,
   stateName     text,
   stateCounter  text,
   lastChange    datetime,
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

INSERT INTO sensor_hits(sensorId, counter) 
SELECT "ESP003", 0
WHERE NOT EXISTS(SELECT 1 FROM sensor_hits WHERE sensorId = "ESP003");


UPDATE sensor_hits
SET counter = counter+1
WHERE sensorId = "ESP001";

UPDATE sensor_hits SET counter = counter+1 WHERE sensorId = "ESP001";


select hits.sensorId,state.sensorId
from sensor_hits as hits
left join sensor_state as state on hits.sensorId = state.sensorId;


insert into sensor_state (sensorId)
SELECT hits.sensorId
from sensor_hits as hits
WHERE NOT EXISTS(SELECT 1 FROM sensor_state as state WHERE hits.sensorId = state.sensorId);


select state.sensorId,hits.sensorId,hits.counter
from sensor_state as state
left join sensor_hits as hits on hits.sensorId = state.sensorId;