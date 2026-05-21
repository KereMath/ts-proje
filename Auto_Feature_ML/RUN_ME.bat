@echo off
echo ====================================================================================================
echo AUTO FEATURE EXTRACTION ML - NO WINDOWING VERSION (12K)
echo ====================================================================================================
echo.
echo This pipeline will:
echo   1. Load balanced samples from each class (12K per class)
echo   2. Extract 700+ features automatically using tsfresh (NO WINDOWING)
echo   3. Train LightGBM, XGBoost, Random Forest, and MLP models
echo   4. Analyze feature importance (overall + per-class)
echo   5. Generate confusion matrices and reports
echo.
echo NO WINDOWING: Each time series = 1 sample (entire series used)
echo Expected time: 60-120 minutes (depending on tsfresh extraction)
echo.
pause

echo.
echo ====================================================================================================
echo STEP 1: FEATURE EXTRACTION (tsfresh)
echo ====================================================================================================
python processor.py
if errorlevel 1 (
    echo [ERROR] Feature extraction failed!
    pause
    exit /b 1
)

echo.
echo ====================================================================================================
echo STEP 2: MODEL TRAINING + FEATURE IMPORTANCE ANALYSIS
echo ====================================================================================================
python trainer.py
if errorlevel 1 (
    echo [ERROR] Training failed!
    pause
    exit /b 1
)

echo.
echo ====================================================================================================
echo PIPELINE COMPLETE!
echo ====================================================================================================
echo.
echo Results saved to:
echo   - Processed data: processed_data_no_window_12k/
echo   - Trained models: trained_models_no_window_12k/
echo   - Reports: reports_no_window_12k/
echo.
echo Check reports_no_window_12k/ for:
echo   - Confusion matrices (PNG)
echo   - Classification reports (JSON)
echo   - Feature importance (overall + per-class)
echo.
pause
