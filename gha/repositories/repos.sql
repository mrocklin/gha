
-- Set up intermediate table
create table important_user_repos  
SELECT  USER_REPOS.repository_owner as repository_owner, 
        USER_REPOS.repository_name as repository_name,
        USER_REPOS.repository_language as repository_language 
FROM 
(  
  SELECT    repository_name  
  FROM github_analysis  
  WHERE repository_forks > 50  
  GROUP BY repository_name  
) as GOOD_REPOS 
INNER JOIN 
(  
  SELECT repository_name, repository_owner, repository_language  
  FROM github_analysis  
  WHERE repository_language != ""  
  GROUP BY repository_name, repository_owner, repository_language  
) as USER_REPOS 
ON GOOD_REPOS.repository_name = USER_REPOS.repository_name 
GROUP BY repository_name, repository_owner, repository_language;

create index important_user_repos1 on important_user_repos (repository_name);
create index important_user_repos2 on important_user_repos (repository_owner);
create index important_user_repos3 on important_user_repos (repository_language);



-- Final result
SELECT  count(T1.repository_owner) as num_users, 
        T1.repository_name,
        T1.repository_language,
        T2.repository_name, 
        T2.repository_language
FROM    important_user_repos as T1  
INNER JOIN
        important_user_repos as T2 
ON T1.repository_owner = T2.repository_owner 
GROUP BY    T1.repository_name, T1.repository_language,
            T2.repository_name, T2.repository_language
ORDER BY num_users DESC;
