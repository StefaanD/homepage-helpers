SELECT
    platform AS value,
    COUNT(DISTINCT COALESCE(reference_id, id))::int AS count
FROM sessions
GROUP BY platform
ORDER BY count DESC
LIMIT 50