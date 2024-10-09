//******* Création de la base de données, des types et des tables

// ********* KEYSPACE *********
CREATE KEYSPACE sink WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true ;

USE sink ;


// ********* TYPES *********

------- Types pour les objets 'album', 'added_by' et 'video_thumbnail' -------

	CREATE TYPE IF NOT EXISTS udt_vidthumbnail (url text) ;

	CREATE TYPE IF NOT EXISTS udt_artists
		(
			external_urls map<text,text>,
			href text,
			id text,
			name text,
			type text,
			uri text
		) ;

	CREATE TYPE IF NOT EXISTS udt_added_by
		(
			external_urls map<text,text>,
			href text,
			id text,
			type text,
			uri text
		) ;


	CREATE TYPE IF NOT EXISTS udt_images
		(
			height smallint,
			url text,
			width smallint
		) ;


	CREATE TYPE IF NOT EXISTS udt_album
		(
			album_type text,
			artists frozen<set<udt_artists>>,
			available_markets set<text>,
			external_urls map<text,text>,
			href text,
			id text,
			images frozen<set <udt_images>>,
			name text,
			release_date date,
			release_date_precision text,
			total_tracks smallint,
			type text,
			uri text
		) ;

	CREATE TYPE IF NOT EXISTS udt_tracks_track
		(
			album frozen<udt_album>,
			artists frozen<set<udt_artists>>,
			available_markets set<text>,
			disc_number smallint,
			duration_ms int,
			episode boolean,
			explicit boolean,
			external_ids map<text,text>,
			external_urls map<text,text>,
			href text,
			id text,
			is_local boolean,
			name text,
			popularity smallint,
			preview_url text,
			track boolean,
			track_number smallint,
			type text,
			uri text
		) ;


	CREATE TYPE IF NOT EXISTS udt_tracks
		(
			added_at timestamp,
			added_by frozen<udt_added_by>,
			is_local boolean,
			primary_color text,
			track frozen<udt_tracks_track>,
			video_thumbnail frozen<udt_vidthumbnail>
		) ;


// ********* TABLE *********

CREATE TABLE IF NOT EXISTS spotify_playlist
	(
		collaborative boolean,
		description text,
		followers int,
		id text,
		name text,
		nbtracks smallint,
		owner text,
		public boolean,
		snapshot_id text,
		tracks frozen<set<udt_tracks>>,
		uri text,
		PRIMARY KEY (id)
	) ;

