CREATE TABLE Commit_Actions
(
    id Varchar[40] NOT NULL PRIMARY KEY,
    action Varchar[4] NOT NULL,
    path Varchar[256] NOT NULL
);

CREATE TABLE Commit_log
(
    author_email Varchar[128],
    author_name  Varchar[128],
    date         DATETIME,
    id           Varchar[40] PRIMARY KEY,
    subject      Varchar[80],
    timestamp    long,
    body         Varchar[256]
);

