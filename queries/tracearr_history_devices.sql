SELECT
    device AS value,
    COUNT(DISTINCT COALESCE(reference_id, id))::int AS count
FROM sessions
GROUP BY device
ORDER BY count DESC
LIMIT 50