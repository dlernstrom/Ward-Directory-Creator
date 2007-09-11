@echo off
cls
echo Did you update the app revision in the following places:
echo 1) The wxs file (3 places),
echo 2) The final filename in this document, and
echo 3) Application.py comments?
echo.
echo Press CTRL-C if you forgot...
echo.
pause
cls
python setup.py py2exe -p email > c:\out.txt
echo Make sure to count the number of files in 2 components of dist (21?)
pause
cls
copy *.jpg dist\*.jpg
copy *.wxs dist\*.wxs
copy *.pdf dist\*.pdf
copy *.rtf dist\*.rtf
cd dist
..\..\Wix\candle.exe WDC_Installer_Wix.wxs
..\..\Wix\light.exe -out ..\WDC-1_0beta132.msi WDC_Installer_Wix.wixobj ..\..\Wix\wixui.wixlib -loc ..\..\Wix\WixUI_en-us.wxl
cd ..
rmdir /s /q build
echo.
echo About to delete the dist folder...
echo.
echo Press CTRL-C to abort
pause
rmdir /s /q dist

