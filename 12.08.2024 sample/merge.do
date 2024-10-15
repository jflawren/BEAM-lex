// Open the CSV file with the first row as variable names
import delimited "/Users/josh/repos/roar_voc/new_assessment_items.csv", clear varnames(1)

// Save as a .dta file
save "/Users/josh/repos/roar_voc/new_assessment_items.dta", replace


// Open the CSV file with the first row as variable names
import delimited "/Users/josh/repos/roar_voc/new_words.csv", clear varnames(1)

// Save as a .dta file
save "/Users/josh/repos/roar_voc/new_words.dta", replace


// Open the new_words.dta file
use "/Users/josh/repos/roar_voc/new_words.dta", clear

// Merge with new_assessment_items.dta using a one-to-many merge on the variable target_word
merge 1:m target_word using "/Users/josh/repos/roar_voc/new_assessment_items.dta"

// Check for merge results (optional)
tab _merge

// Drop the _merge variable if no longer needed
drop _merge

// Sort the dataset by target_word
sort target_word

// Create the target_n variable that counts the occurrences of each target_word
by target_word: gen target_n = _n


<// Save the merged dataset
save "/Users/josh/repos/roar_voc/merged_data.dta", replace


 export delimited using "/Users/josh/repos/roar_voc/merged 12.08.2024.csv", replace
