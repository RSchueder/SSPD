
rem for /F "delims=" %%i in ('dir /b') do (rmdir "%%i" /s/q || del "%%i" /s/q)
rem rmdir "C:\Solutions\PFAS\" /s /q

rem if not exist "C:\Solutions\PFAS\" mkdir "C:\Solutions\PFAS\"

rmdir "C:\Solutions\Scen\emissiondata\" /s /q
xcopy /s /q "p:\1209104-solutions\WP14\SIM\_Prod\emissiondata" "C:\Solutions\Scen\emissiondata\" 

rmdir "C:\Solutions\Scen\substanceproperties\" /s /q
xcopy /s /q "p:\1209104-solutions\WP14\SIM\_Prod\substanceproperties" "C:\Solutions\Scen\substanceproperties\"

rmdir "C:\Solutions\Scen\EP_Europe_PFAS\"  /s /q
xcopy /s /q "p:\1209104-solutions\WP14\SIM\_Prod\EP_Europe_PFAS" "C:\Solutions\Scen\EP_Europe_PFAS\" 

rmdir "C:\Solutions\Scen\QP_RhineChF_PFAS\"  /s /q
xcopy /s /q "p:\1209104-solutions\WP14\SIM\_Prod\QP_RhineChF_PFAS" "C:\Solutions\Scen\QP_RhineChF_PFAS\" 
rmdir "C:\Solutions\Scen\QP_RhineChF_PFAS\subout"  /s /q
mkdir C:\Solutions\Scen\QP_RhineChF_PFAS\subout

rmdir "C:\Solutions\Scen\_ProdPFAS\"  /s /q
xcopy /s /q "p:\1209104-solutions\WP14\SIM\_Prod\_nodes\_Prod%1" "C:\Solutions\Scen\_ProdPFAS\" 

cd ..\Scen\_ProdPFAS\

call run%1_PFAS
rem call copy%1_SCN%2_ChF

rem