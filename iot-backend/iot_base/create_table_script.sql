CREATE TABLE events (
	id serial4 NOT NULL,
	device varchar NOT NULL,
	"timestamp" timestamp NULL,
	event_type varchar NOT NULL,
	event_data float NOT NULL,
	CONSTRAINT events_pkey PRIMARY KEY (id)
);