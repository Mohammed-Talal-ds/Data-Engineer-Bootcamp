INSERT INTO dim_date (
    date_id, full_date, day, month, year, quarter, weekday,
    is_weekend, is_ramadan, is_eid_al_fitr, is_eid_al_adha
)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INT AS date_id,
    d AS full_date,
    EXTRACT(DAY FROM d),
    EXTRACT(MONTH FROM d),
    EXTRACT(YEAR FROM d),
    EXTRACT(QUARTER FROM d),
    TO_CHAR(d, 'Day'),

    CASE WHEN EXTRACT(ISODOW FROM d) IN (6,7) THEN TRUE ELSE FALSE END,

    -- 🌙 RAMADAN (approx yearly windows)
    CASE 
        WHEN (d BETWEEN '2020-04-24' AND '2020-05-23') OR
             (d BETWEEN '2021-04-13' AND '2021-05-12') OR
             (d BETWEEN '2022-04-02' AND '2022-05-01') OR
             (d BETWEEN '2023-03-23' AND '2023-04-21') OR
             (d BETWEEN '2024-03-11' AND '2024-04-09') OR
             (d BETWEEN '2025-03-01' AND '2025-03-30') OR
             (d BETWEEN '2026-02-18' AND '2026-03-19')
        THEN TRUE ELSE FALSE
    END,

    -- 🌙 Eid al-Fitr (1–3 days after Ramadan)
    CASE 
        WHEN d IN (
            '2020-05-24','2020-05-25','2020-05-26',
            '2021-05-13','2021-05-14','2021-05-15',
            '2022-05-02','2022-05-03','2022-05-04',
            '2023-04-22','2023-04-23','2023-04-24',
            '2024-04-10','2024-04-11','2024-04-12',
            '2025-03-31','2025-04-01','2025-04-02'
        )
        THEN TRUE ELSE FALSE
    END,

    CASE 
        WHEN d IN (
            '2020-07-31','2020-08-01','2020-08-02','2020-08-03',
            '2021-07-20','2021-07-21','2021-07-22','2021-07-23',
            '2022-07-09','2022-07-10','2022-07-11','2022-07-12',
            '2023-06-28','2023-06-29','2023-06-30','2023-07-01',
            '2024-06-16','2024-06-17','2024-06-18','2024-06-19',
            '2025-06-05','2025-06-06','2025-06-07','2025-06-08'
        )
        THEN TRUE ELSE FALSE
    END

FROM generate_series(
    '2020-01-01'::DATE,
    '2050-12-31'::DATE,
    INTERVAL '1 day'
) d;