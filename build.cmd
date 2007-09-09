echo "Did you update the app revision in both the wxs file (2 places), this document, and Application.py comments?"
pause

python setup.py py2exe -p email > c:\out.txt
copy *.jpg dist\*.jpg
copy *.wxs dist\*.wxs
copy Manual.pdf dist\Manual.pdf
..\Wix\candle.exe dist\WDC_Installer_Wix.wxs
..\Wix\light.exe -out WDC-1_0beta129.msi WDC_Installer_Wix.wixobj ..\Wix\wixui.wixlib -loc ..\Wix\WixUI_en-us.wxl
pause