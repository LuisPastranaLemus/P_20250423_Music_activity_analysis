/* Postgre Query
da_shl_spr_music_activity */

-- Table Overview
SELECT * 
FROM da_shl_spr_music_activity;



-- Check column's names
SELECT 
    column_name
FROM 
    information_schema.columns
WHERE 
    table_schema = 'public' 
    AND table_name = 'da_shl_spr_music_activity'
ORDER BY ordinal_position;



-- Check chars before column name
SELECT 
    column_name,
    ascii(column_name) as first_char_ascii,
    length(column_name) as name_length
FROM information_schema.columns 
WHERE table_schema = 'public' 
  AND table_name = 'da_shl_spr_music_activity'
ORDER BY ordinal_position;



-- Modify column name
ALTER TABLE public.da_shl_spr_music_activity 
RENAME COLUMN "  userID" TO user_id;

ALTER TABLE public.da_shl_spr_music_activity 
RENAME COLUMN "  City  " TO city;

ALTER TABLE public.da_shl_spr_music_activity 
RENAME COLUMN "Track" TO track;

ALTER TABLE public.da_shl_spr_music_activity 
RENAME COLUMN "Day" TO day;



-- Select some columns from table
SELECT track, artist, genre  
FROM public.da_shl_spr_music_activity;



-- Delete blank spaces before and after a string within the registries
UPDATE public.da_shl_spr_music_activity 
SET user_id = TRIM(user_id),
    track = TRIM(track),
    artist = TRIM(artist),
    genre = TRIM(genre),
    city = TRIM(city),
    time = TRIM(time),
    day = TRIM(day);

/*  TRIM(columna) - delete blank spaces both sides
    LTRIM(columna) - delete blank spaces left side
    RTRIM(columna) - delete blank spaces right side
    TRIM(BOTH FROM columna) - same as TRIM() */



-- Show total amount of explicit duplicates
SELECT 
    COUNT(*) as total_duplicated_groups,
    SUM(duplicates_amount) as total_duplicate_records,
    SUM(duplicates_amount - 1) as total_surplus
FROM (SELECT COUNT(*) as duplicates_amount
      FROM public.da_shl_spr_music_activity
      GROUP BY user_id, track, artist, genre, city, time, day
      HAVING COUNT(*) > 1) groups;


-- Show explicit duplicates
SELECT *
FROM public.da_shl_spr_music_activity
WHERE (user_id, track, artist, genre, city, time, day) 
    IN (SELECT user_id, track, artist, genre, city, time, day
        FROM public.da_shl_spr_music_activity
        GROUP BY user_id, track, artist, genre, city, time, day
        HAVING COUNT(*) > 1)
ORDER BY user_id;



-- Delete explicit duplicates

SELECT COUNT(*) as total_before 
FROM public.da_shl_spr_music_activity;

DELETE FROM public.da_shl_spr_music_activity
WHERE ctid IN (SELECT ctid
               FROM (SELECT ctid, ROW_NUMBER() OVER (PARTITION BY user_id, track, artist, genre, city, time, day
                                                     ORDER BY ctid) as rn
                     FROM public.da_shl_spr_music_activity) t
                WHERE t.rn > 1);  -- Keeps the first, delete the rest

SELECT COUNT(*) as total_after 
FROM public.da_shl_spr_music_activity;