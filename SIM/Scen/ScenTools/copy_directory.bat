
rem for /F "delims=" %%i in ('dir /b') do (rmdir "%%i" /s/q || del "%%i" /s/q)
rmdir "C:\Solutions\Scen\" /s /q

if not exist "C:\Solutions\Scen\" mkdir "C:\Solutions\Scen\"

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\Delwaq.std" "C:\Solutions\Scen\Delwaq.std\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\Delwaq.win64_Oct2016" "C:\Solutions\Scen\Delwaq.win64_Oct2016\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\Emis" "C:\Solutions\Scen\Emis\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\emissiondata" "C:\Solutions\Scen\emissiondata\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\EP_EuropeScen" "C:\Solutions\Scen\EP_EuropeScen\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\HN_Europe" "C:\Solutions\Scen\HN_Europe\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\HN_RhineAQ" "C:\Solutions\Scen\HN_RhineAQ\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\HOC2" "C:\Solutions\Scen\HOC2\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\OpenPB.ESpace" "C:\Solutions\Scen\OpenPB.Espace\" 
 
xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\OpenPB.Fug6" "C:\Solutions\Scen\OpenPB.Fug6\" 

xcopy "p:\1209104-solutions\WP14\SIM\_Scen\QP_RhineChF" "C:\Solutions\Scen\QP_RhineChF\" 
mkdir C:\Solutions\Scen\QP_RhineChF\subout%2

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\substanceproperties" "C:\Solutions\Scen\substanceproperties\"

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\scalFiles" "c:\Solutions\Scen\scalFiles\"

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\Tools" "C:\Solutions\Scen\Tools\" 

xcopy /s "p:\1209104-solutions\WP14\SIM\_Scen\_nodes\_Prod%1" "C:\Solutions\Scen\_ProdScen\" 

cd ..\Scen\_ProdScen\

call run%1_SCN%2_ChF
rem call copy%1_SCN%2_ChF