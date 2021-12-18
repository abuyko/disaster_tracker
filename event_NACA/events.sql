create
extension cube;
create
extension earthdistance;

CREATE TABLE events
(
    id                   SERIAL PRIMARY KEY,
    event_id             VARCHAR(255) NOT NULL,
    event_title          VARCHAR(255),
    event_description    VARCHAR(255),
    event_link           VARCHAR(255),
    event_closed         VARCHAR(255),
    event_categories     VARCHAR(255),
    event_magnitudeValue VARCHAR(255),
    event_magnitudeUnit  VARCHAR(255),
    event_date           timestamp,
    event_type           VARCHAR(255),
    event_coordinates    point

);


INSERT INTO events(event_id, event_title, event_description, event_link, event_closed, event_categories,
                   event_magnitudeValue, event_magnitudeUnit, event_date, event_type, event_coordinates)
VALUES ('EONET_5979', 'Tropical Cyclone Teratai', NULL, 'https://eonet.gsfc.nasa.gov/api/v3/events/EONET_5979', NULL,
        '[{"id": "severeStorms", "title": "Severe Storms"}]', '35', 'kts', '2021-11-30 18:00:00', 'Point',
        '(102.8, -8.0)')
;


select *, (point(0, 0) < @ > events.event_coordinates) as distance
from events
where event_date >= '2021-12-13 18:00:00'
  and event_date <= '2021-12-18 18:00:00';

