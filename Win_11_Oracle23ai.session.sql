/* Oracle Query
DA_SHL_SPR_MUSIC_ACTIVITY */

-- Table Overview
SELECT *
FROM DA_SHL_SPR_MUSIC_ACTIVITY;



-- Check column's names
SELECT 
    column_name
FROM 
    all_tab_columns
WHERE owner = 'LUIS'
  AND table_name = 'DA_SHL_SPR_MUSIC_ACTIVITY'
ORDER BY COLUMN_ID;



-- Check chars before column name
SELECT 
    column_name,
    ASCII(SUBSTR(column_name, 1, 1)) as first_char_ascii,
    LENGTH(column_name) as name_length
FROM all_tab_columns 
WHERE owner = 'LUIS' 
  AND table_name = 'DA_SHL_SPR_MUSIC_ACTIVITY'
ORDER BY COLUMN_ID;



-- Modify column name
ALTER TABLE LUIS.DA_SHL_SPR_MUSIC_ACTIVITY 
RENAME COLUMN "  userID" TO "user_id";

ALTER TABLE LUIS.DA_SHL_SPR_MUSIC_ACTIVITY 
RENAME COLUMN "  City  " TO "city";

ALTER TABLE LUIS.DA_SHL_SPR_MUSIC_ACTIVITY 
RENAME COLUMN "Track" TO "track";

ALTER TABLE LUIS.DA_SHL_SPR_MUSIC_ACTIVITY 
RENAME COLUMN "Day" TO "day";



-- Select some columns from table
SELECT "track", "artist", "genre"
FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY;



-- Delete blank spaces before and after a string within the registries
UPDATE LUIS.DA_SHL_SPR_MUSIC_ACTIVITY 
SET "user_id" = TRIM("user_id"),
    "track" = TRIM("track"),
    "artist" = TRIM("artist"),
    "genre" = TRIM("genre"),
    "city" = TRIM("city"),
    "time" = TRIM("time"),
    "day" = TRIM("day");

/*  TRIM(columna) - delete blank spaces both sides
    LTRIM(columna) - delete blank spaces left side
    RTRIM(columna) - delete blank spaces right side
    TRIM(BOTH ' ' FROM columna) - delete specific blank spaces */



-- Show total amount of explicit duplicates
SELECT 
    COUNT(*) as "total_duplicated_groups",
    SUM("duplicates_amount") as "total_duplicate_records",
    SUM("duplicates_amount" - 1) as "total_surplus"
FROM (SELECT COUNT(*) as "duplicates_amount"
      FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY
      GROUP BY "user_id", "track", "artist", "genre", "city", "time", "day"
      HAVING COUNT(*) > 1) groups;



-- Show explicit duplicates
SELECT *
FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY
WHERE ("user_id", "track", "artist", "genre", "city", "time", "day") 
    IN (SELECT "user_id", "track", "artist", "genre", "city", "time", "day"
        FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY
        GROUP BY "user_id", "track", "artist", "genre", "city", "time", "day"
        HAVING COUNT(*) > 1)
ORDER BY "user_id";



-- Delete explicit duplicates
SELECT COUNT(*) as total_before 
FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY;

DELETE FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY
WHERE ROWID IN (SELECT ROWID
                FROM (SELECT ROWID, ROW_NUMBER() OVER (PARTITION BY "user_id", "track", "artist", "genre", "city", "time", "day"
                                                       ORDER BY ROWID) as rn
                      FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY) t
                WHERE t.rn > 1);  -- Keeps the first, deletes the rest

SELECT COUNT(*) as total_after 
FROM LUIS.DA_SHL_SPR_MUSIC_ACTIVITY;


-- Verify that you have DELETE permissions
SELECT * FROM USER_TAB_PRIVS 
WHERE TABLE_NAME = 'DA_SHL_SPR_MUSIC_ACTIVITY';

-- Check if there are locks in the table
SELECT * FROM V$LOCKED_OBJECT 
WHERE OBJECT_NAME = 'DA_SHL_SPR_MUSIC_ACTIVITY';