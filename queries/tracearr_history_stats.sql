SELECT
    COUNT(DISTINCT COALESCE(reference_id, id))::int as play_count,
    COALESCE(SUM(duration_ms), 0)::bigint as total_watch_time_ms,
    COUNT(DISTINCT server_user_id)::int as unique_users,
    COUNT(DISTINCT media_title) as unique_content
FROM sessions