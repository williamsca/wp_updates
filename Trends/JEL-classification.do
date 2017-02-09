cd C:\Users\Colin\Desktop\ComputerTA\RePEc_Update\Trends
set more off

clear
import delimited JEL-classification.csv, varnames(1)

drop if keyword == ""
