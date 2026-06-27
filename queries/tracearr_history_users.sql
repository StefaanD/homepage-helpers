SELECT
    su.username,
    su.thumb_url,
    COUNT(
        DISTINCT COALESCE(
            s.reference_id,
            s.id
        )
    )::int AS count
FROM sessions s
JOIN server_users su
    ON su.id = s.server_user_id
GROUP BY
    su.username,
    su.thumb_url
ORDER BY count DESC;