cd C:\Users\Colin\Desktop\ComputerTA\RePEc_Update\Trends
set more off

clear
import delimited keywords.csv, varnames(1)

drop if keyword == ""

gen Z=lower(keyword)
drop keyword
rename Z keyword

drop 

gen freq = 1
graph bar (sum) freq, over(keyword) sort()
