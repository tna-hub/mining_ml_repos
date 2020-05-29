CREATE SEQUENCE "public".commit_modifications_id_seq START WITH 1;

CREATE SEQUENCE "public".commits_id_seq START WITH 1;

CREATE SEQUENCE "public".datasets_key_column_seq START WITH 1;

CREATE SEQUENCE "public".element_key_column_seq START WITH 1;

CREATE  TABLE "public".repos ( 
	id                   integer  NOT NULL ,
	link                 varchar(5000)  NOT NULL ,
	nb_commits           integer   ,
	name                 varchar(500)   ,
	folder_name          varchar(500)   ,
	CONSTRAINT pk_repos_id PRIMARY KEY ( id )
 );

COMMENT ON TABLE "public".repos IS 'Repositories to analyse';

COMMENT ON COLUMN "public".repos.link IS 'Github link';

COMMENT ON COLUMN "public".repos.nb_commits IS 'Total commits in the repository';

CREATE  TABLE "public".commits ( 
	id                   serial  NOT NULL ,
	repo_id              integer  NOT NULL ,
	sha                  varchar  NOT NULL ,
	commit_date          timestamp   ,
	author_name          varchar   ,
	author_email         varchar   ,
	total_modifs         integer   ,
	CONSTRAINT pk_commits_id PRIMARY KEY ( id )
 );

CREATE  TABLE "public".element ( 
	id                   serial  NOT NULL ,
	name                 varchar(500)   ,
	is_code_file         bool   ,
	ast                  json   ,
	repo_id              integer   ,
	is_folder            bool  NOT NULL ,
	extension            varchar   ,
	CONSTRAINT element_pkey PRIMARY KEY ( id )
 );

COMMENT ON TABLE "public".element IS 'Information of files of folders in the repositories';

COMMENT ON COLUMN "public".element.is_code_file IS 'Set to True or False if file has code or not';

COMMENT ON COLUMN "public".element.ast IS 'json ast of the file''s code';

COMMENT ON COLUMN "public".element.is_folder IS 'True if it is a folder, false if it is not';

CREATE  TABLE "public".commit_modifications ( 
	id                   serial  NOT NULL ,
	file_id              integer  NOT NULL ,
	change_type          varchar   ,
	commit_id            integer   ,
	CONSTRAINT pk_commit_modifications_id PRIMARY KEY ( id )
 );

CREATE  TABLE "public".datasets ( 
	id                   serial  NOT NULL ,
	element_id           integer  NOT NULL ,
	heuristic            varchar(2)  NOT NULL ,
	file_mention         integer  NOT NULL ,
	repo_id              integer  NOT NULL ,
	CONSTRAINT datasets_pkey PRIMARY KEY ( id )
 );

COMMENT ON COLUMN "public".datasets.heuristic IS 'The heuristic used to identify as dataset';

COMMENT ON COLUMN "public".datasets.file_mention IS 'The file where the dataset is loaded';

ALTER TABLE "public".commit_modifications ADD CONSTRAINT fk_commit_modifications_commits FOREIGN KEY ( commit_id ) REFERENCES "public".commits( id );

ALTER TABLE "public".commit_modifications ADD CONSTRAINT fk_commit_modifications_element FOREIGN KEY ( file_id ) REFERENCES "public".element( id );

ALTER TABLE "public".commits ADD CONSTRAINT fk_commits_repos FOREIGN KEY ( repo_id ) REFERENCES "public".repos( id );

ALTER TABLE "public".datasets ADD CONSTRAINT fk_datasets_element FOREIGN KEY ( element_id ) REFERENCES "public".element( id );

ALTER TABLE "public".datasets ADD CONSTRAINT fk_datasets_element_0 FOREIGN KEY ( file_mention ) REFERENCES "public".element( id );

ALTER TABLE "public".datasets ADD CONSTRAINT fk_datasets_repos FOREIGN KEY ( repo_id ) REFERENCES "public".repos( id );

ALTER TABLE "public".element ADD CONSTRAINT fk_element_repos FOREIGN KEY ( repo_id ) REFERENCES "public".repos( id );
