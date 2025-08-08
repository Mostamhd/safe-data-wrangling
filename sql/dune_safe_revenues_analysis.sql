-- Step 1: categorize the data
WITH cleaned_data AS (
  SELECT 
    tx_hash,
    feature,
    trader,
    is_stablecoin_pair,
    usd_value,
    block_date,
    
    CASE 
      WHEN feature IN ('native swaps', 'native swaps lifi') THEN 'native_swaps'
      WHEN feature = 'cow safeapp' THEN 'cow_safeapp'
      WHEN feature = 'oneinch safeapp' THEN 'oneinch_safeapp' 
      WHEN feature = 'kyberswap' THEN 'kyberswap'
      ELSE 'other'
    END AS feature_category
    
  FROM dune.safe.result_testset
  WHERE usd_value > 0
),

-- Step 2: Calculate fee rates
fee_rates AS (
  SELECT *,

    CASE 
      WHEN feature_category = 'native_swaps' AND is_stablecoin_pair = 1 AND usd_value <= 100000 THEN 0.0010
      WHEN feature_category = 'native_swaps' AND is_stablecoin_pair = 1 AND usd_value <= 1000000 THEN 0.0007  
      WHEN feature_category = 'native_swaps' AND is_stablecoin_pair = 1 THEN 0.0005
      WHEN feature_category = 'native_swaps' AND is_stablecoin_pair = 0 AND usd_value <= 100000 THEN 0.0035
      WHEN feature_category = 'native_swaps' AND is_stablecoin_pair = 0 AND usd_value <= 1000000 THEN 0.0020
      WHEN feature_category = 'native_swaps' AND is_stablecoin_pair = 0 THEN 0.0010

      WHEN feature_category = 'cow_safeapp' THEN 0.00045
      WHEN feature_category = 'oneinch_safeapp' THEN 0.00053
      WHEN feature_category = 'kyberswap' THEN 0.00045
      ELSE 0
    END AS fee_rate
  FROM cleaned_data
),

-- Step 3: Calculate revenue
revenue_data AS (
  SELECT *,
    usd_value * fee_rate AS revenue_usd
  FROM fee_rates
)

-- Step 4: Final results with clear breakdown
SELECT 
  'TOTAL' as summary_type,
  NULL as feature,
  NULL as is_stablecoin_pair,
  ROUND(SUM(revenue_usd), 2) as revenue_usd,
  COUNT(*) as transactions,
  ROUND(SUM(usd_value), 2) as volume_usd,
  ROUND(SUM(revenue_usd) / SUM(usd_value) * 100, 4) as avg_fee_pct
FROM revenue_data

UNION ALL

SELECT 
  'BY_FEATURE' as summary_type,
  feature_category,
  NULL as is_stablecoin_pair,
  ROUND(SUM(revenue_usd), 2) as revenue_usd,
  COUNT(*) as transactions,
  ROUND(SUM(usd_value), 2) as volume_usd,
  ROUND(SUM(revenue_usd) / SUM(usd_value) * 100, 4) as avg_fee_pct
FROM revenue_data
GROUP BY feature_category

UNION ALL

SELECT 
  'BY_FEATURE_AND_PAIR' as summary_type,
  feature_category,
  is_stablecoin_pair,
  ROUND(SUM(revenue_usd), 2) as revenue_usd,
  COUNT(*) as transactions,
  ROUND(SUM(usd_value), 2) as volume_usd,
  ROUND(SUM(revenue_usd) / SUM(usd_value) * 100, 4) as avg_fee_pct
FROM revenue_data
GROUP BY feature_category, is_stablecoin_pair

ORDER BY summary_type, feature, is_stablecoin_pair;