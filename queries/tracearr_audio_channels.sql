SELECT
    COALESCE(
        audio_channels,
        0
    ) AS channels,
    COUNT(*) AS count
FROM library_items
WHERE media_type IN (
    'movie',
    'episode'
)
GROUP BY channels
ORDER BY count DESC;