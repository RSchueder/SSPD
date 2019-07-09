set case=Rhine


if not exist ..\subout\%1_Cdis.csv goto end

..\..\tools\DWQ2Stat.exe %1 ..\subout\%1_Cdis.csv ..\..\HN_%case%\stores.def ..\..\HN_%case%\scalist.inc OLK CDis stats%1.csv 366  onlyyear

if not exist stats%1.csv goto end

echo %1 >> caslist


:end
