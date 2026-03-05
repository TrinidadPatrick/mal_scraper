@echo off
setlocal enabledelayedexpansion

set "option[1]=scrape_top_animes"
set "option[2]=scrape_recommended_animes"
set "option[3]=scrape_seasonal_animes"
set "option[4]=scrape_scheduled_animes"
set "option[5]=scrape_characters"
set "option[6]=Clear"
set "option[7]=Exit"

:menu
cls
echo ============================================
echo           MAL INTEGRATION TOOLS
echo ============================================
echo Enter numbers separated by spaces (e.g., 1 3 4) if you want multiple options
echo.

for /L %%i in (1,1,7) do (
    echo [%%i] !option[%%i]!
)

echo.
set /p "choices=Select which category to scrape: "

@REM Year selector for seasonal anime
set "needYear=0"
for %%c in (%choices%) do (
    if "%%c"=="3" set "needYear=1"
)

if "!needYear!"=="1" (
    echo.
    set /p "year=Select which year to start scraping: "
)

@REM Page limit selector for top animes
set "needTopAnimePage=0"
for %%c in (%choices%) do (
    if "%%c"=="1" set "needTopAnimePage=1"
)

if "!needTopAnimePage!"=="1" (
    echo.
    set /p "TopAnimepageLimit=Please specify how many page per top anime to fetch (Each page is 50 animes): "
)

@REM Page limit selector for characters
set "needCharactersPage=0"
for %%c in (%choices%) do (
    if "%%c"=="5" set "needCharactersPage=1"
)

if "!needCharactersPage!"=="1" (
    echo.
    set /p "CharacterspageLimit=Please specify how many page per characters to fetch (Each page is 50 characters): "
)

for %%c in (%choices%) do (
    set "found=0"
    if "%%c"=="1" ( set "found=1" & call :scrape_top_animes !TopAnimepageLimit! )
    if "%%c"=="2" ( set "found=1" & call :scrape_recommended_animes )
    if "%%c"=="3" ( set "found=1" & call :scrape_seasonal_animes !year! )
    if "%%c"=="4" ( set "found=1" & call :scrape_scheduled_animes)
    if "%%c"=="5" ( set "found=1" & call :scrape_characters !CharacterspageLimit!)
    if "%%c"=="6" ( set "found=1" & call :clear )
    if "%%c"=="7" ( set "found=1" & exit )

    if "!found!"=="0" (
        echo.
        echo Option %%c does not exist. Skipping...
        timeout /t 2 >nul
    )
)

echo.
echo All tasks finished.
pause
goto :menu

:scrape_top_animes
echo.
echo ============================================
echo Running scrape_top_animes script...
echo ============================================
echo.
python main.py scrape_top_animes %1
exit /b

:scrape_recommended_animes
echo.
echo ============================================
echo Running scrape_recommended_animes script...
echo ============================================
echo.
python main.py scrape_recommended_animes
exit /b

:scrape_seasonal_animes
echo.
echo ============================================
echo Running scrape_seasonal_animes script...
echo ============================================
echo.
python main.py scrape_seasonal_animes %1
exit /b

:scrape_scheduled_animes
echo.
echo ============================================
echo Running scrape_scheduled_animes script...
echo ============================================
echo.
python main.py scrape_scheduled_animes
exit /b

:scrape_characters
echo.
echo ============================================
echo Running scrape_characters script...
echo ============================================
echo.
python main.py scrape_characters %1
exit /b


