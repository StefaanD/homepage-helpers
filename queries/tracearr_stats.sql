WITH latest_snapshots AS (
    SELECT DISTINCT ON (ls.server_id, ls.library_id)
        ls.item_count,
        ls.total_size,
        ls.movie_count,
        ls.episode_count,
        ls.show_count,
        ls.season_count,
        ls.music_count,
        ls.count_4k,
        ls.count_1080p,
        ls.count_720p,
        ls.count_sd,
        ls.snapshot_time
    FROM library_snapshots ls
    ORDER BY
        ls.server_id,
        ls.library_id,
        ls.snapshot_time DESC
)

SELECT
    COALESCE(SUM(item_count), 0)::int AS total_items,
    COALESCE(SUM(total_size), 0)::bigint AS total_size_bytes,
    COALESCE(SUM(movie_count), 0)::int AS movie_count,
    COALESCE(SUM(episode_count), 0)::int AS episode_count,
    COALESCE(SUM(show_count), 0)::int AS show_count,
    COALESCE(SUM(season_count), 0)::int AS season_count,
    COALESCE(SUM(music_count), 0)::int AS music_count,
    COALESCE(SUM(count_4k), 0)::int AS count_4k,
    COALESCE(SUM(count_1080p), 0)::int AS count_1080p,
    COALESCE(SUM(count_720p), 0)::int AS count_720p,
    COALESCE(SUM(count_sd), 0)::int AS count_sd
FROM latest_snapshots;