-- Pipeline v3 — Analysis SQL Queries
-- All queries used in Stage 2 verification (CRITIC-CHECK)
-- Author: Anonymous Author
-- Date: 2026-06-07

-- ============================================================
-- DATABASE: db/survey.db
-- TABLE: survey
-- ============================================================

-- Schema check
SELECT name FROM sqlite_master WHERE type='table';
PRAGMA table_info(survey);

-- ============================================================
-- QUERY 1: Row count
-- ============================================================
SELECT COUNT(*) AS total_rows FROM survey;
-- Expected: 65437

-- ============================================================
-- QUERY 2: AIThreat=Yes group — N, mean JobSat, SD
-- ============================================================
SELECT
    COUNT(*) AS n,
    ROUND(AVG(JobSat), 4) AS mean_jobsat,
    ROUND(SQRT(AVG(JobSat*JobSat) - AVG(JobSat)*AVG(JobSat)), 4) AS sd_jobsat
FROM survey
WHERE AIThreat = 'Yes'
  AND JobSat IS NOT NULL
  AND AIAcc IS NOT NULL AND AIAcc NOT IN ('NA', '')
  AND WorkExp IS NOT NULL AND WorkExp NOT IN ('NA', '')
  AND YearsCodePro IS NOT NULL AND YearsCodePro NOT IN ('NA', '');
-- Expected: N=1846, Mean=6.4231, SD≈2.2968

-- ============================================================
-- QUERY 3: AIThreat=No+Unsure group — N, mean JobSat, SD
-- ============================================================
SELECT
    COUNT(*) AS n,
    ROUND(AVG(JobSat), 4) AS mean_jobsat,
    ROUND(SQRT(AVG(JobSat*JobSat) - AVG(JobSat)*AVG(JobSat)), 4) AS sd_jobsat
FROM survey
WHERE (AIThreat = 'No' OR AIThreat = 'I''m not sure')
  AND JobSat IS NOT NULL
  AND AIAcc IS NOT NULL AND AIAcc NOT IN ('NA', '')
  AND WorkExp IS NOT NULL AND WorkExp NOT IN ('NA', '')
  AND YearsCodePro IS NOT NULL AND YearsCodePro NOT IN ('NA', '');
-- Expected: N=15824, Mean=7.0468, SD≈2.0293

-- ============================================================
-- QUERY 4: Total listwise N (main model)
-- ============================================================
SELECT COUNT(*) AS listwise_n
FROM survey
WHERE JobSat IS NOT NULL
  AND AIThreat IS NOT NULL AND AIThreat NOT IN ('NA', '')
  AND AIAcc IS NOT NULL AND AIAcc NOT IN ('NA', '')
  AND WorkExp IS NOT NULL AND WorkExp NOT IN ('NA', '')
  AND YearsCodePro IS NOT NULL AND YearsCodePro NOT IN ('NA', '');
-- Expected: 17670

-- ============================================================
-- QUERY 5: AIAcc → JobSat — sample stats
-- ============================================================
SELECT
    COUNT(*) AS n,
    ROUND(AVG(
        CASE AIAcc
            WHEN 'Highly distrust' THEN 1
            WHEN 'Somewhat distrust' THEN 2
            WHEN 'Neither trust nor distrust' THEN 3
            WHEN 'Somewhat trust' THEN 4
            WHEN 'Highly trust' THEN 5
        END
    ), 4) AS mean_aiaccord,
    ROUND(AVG(JobSat), 4) AS mean_jobsat
FROM survey
WHERE AIAcc NOT IN ('NA', '') AND AIAcc IS NOT NULL
  AND JobSat IS NOT NULL;
-- Expected: N≈18215, Mean_AIAcc≈3.009, Mean_JobSat≈6.970

-- ============================================================
-- QUERY 6: Missing value rates for key columns
-- ============================================================
SELECT
    'JobSat' AS col,
    SUM(CASE WHEN JobSat IS NULL THEN 1 ELSE 0 END) AS n_missing,
    ROUND(100.0 * SUM(CASE WHEN JobSat IS NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_missing
FROM survey
UNION ALL
SELECT 'AIThreat' AS col,
    SUM(CASE WHEN AIThreat IS NULL OR AIThreat='NA' THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN AIThreat IS NULL OR AIThreat='NA' THEN 1 ELSE 0 END) / COUNT(*), 1)
FROM survey
UNION ALL
SELECT 'AIAcc' AS col,
    SUM(CASE WHEN AIAcc IS NULL OR AIAcc='NA' THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN AIAcc IS NULL OR AIAcc='NA' THEN 1 ELSE 0 END) / COUNT(*), 1)
FROM survey;

-- ============================================================
-- QUERY 7: AISelect distribution
-- ============================================================
SELECT AISelect, COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM survey), 1) AS pct
FROM survey
GROUP BY AISelect
ORDER BY n DESC;

-- ============================================================
-- QUERY 8: JobSat distribution
-- ============================================================
SELECT
    ROUND(MIN(JobSat), 0) AS min_jobsat,
    ROUND(MAX(JobSat), 0) AS max_jobsat,
    ROUND(AVG(JobSat), 3) AS mean_jobsat,
    COUNT(JobSat) AS n_non_null
FROM survey;
