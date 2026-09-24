BEGIN TRANSACTION;
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
INSERT INTO "admin" VALUES(1,'admin','$2b$12$ARlLc4Q4dhZ0PG4sNOQIN.bM65ZHVPtLrgtD4Lu2fh89hb9lZn0a.');
CREATE TABLE lexicon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    english TEXT NOT NULL,
    swahili TEXT NOT NULL,
    category TEXT
);
INSERT INTO "lexicon" VALUES(13,'Hello','Habari','greeting');
INSERT INTO "lexicon" VALUES(14,'Book','Kitabu','object');
INSERT INTO "lexicon" VALUES(15,'Water','Maji','nature');
INSERT INTO "lexicon" VALUES(16,'Love','Upendo','emotion');
INSERT INTO "lexicon" VALUES(17,'Computer','Kompyuta','technology');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('admin',1);
INSERT INTO "sqlite_sequence" VALUES('lexicon',22);
COMMIT;
