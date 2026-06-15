SELECT
    COALESCE(
        UPPER(audio_codec),
        'unknown'
    ) AS codec,
    COUNT(*) AS count
FROM library_items
WHERE media_type IN (
    'movie',
    'episode'
)
GROUP BY codec
ORDER BY count DESC;