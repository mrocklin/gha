-- Language connections
-- I named the main table github_timeline in my database. 
-- It is called [githubarchive:github.timeline] on BigQuery

-- Table of the language every owner knows. Looks like
-- gvrossum Python
-- gvrossum C
-- coolkid  Perl
CREATE TABLE owner_lang
SELECT DISTINCT repository_owner, repository_language
FROM   github_timeline
WHERE  repository_language != "";
-- We're going to perform some all-to-all queries on this table, might as well
-- make some indices for it
create index owner_lang_owner on owner_lang (repository_owner);
create index owner_lang_lang on owner_lang (repository_language);

-- Final result
-- Pull out the number of users that use both languages A and B
-- looks like
-- 64000 JavaScript JavaScript
-- 48000 Ruby Ruby
-- 12000 JavaScript Ruby (i.e. 12000 people use both JavaScript and Ruby)
SELECT  count(T1.repository_owner) as num_users, 
        T1.repository_language,
        T2.repository_language
FROM        owner_lang as T1
INNER JOIN  owner_lang as T2
ON          T1.repository_owner = T2.repository_owner
GROUP BY T1.repository_language, T2.repository_language
ORDER BY num_users DESC;
