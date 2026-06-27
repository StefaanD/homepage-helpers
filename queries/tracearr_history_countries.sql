SELECT
    geo_country AS value,
    COUNT(DISTINCT COALESCE(reference_id, id))::int AS count
FROM sessions
GROUP BY geo_country
ORDER BY count DESC
LIMIT 250