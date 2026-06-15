SELECT
    COALESCE(
        LOWER(video_resolution),
        'unknown'
    ) AS resolution,
    COUNT(*) AS count
FROM library_items
WHERE media_type='movie'
GROUP BY resolution
ORDER BY count DESC;