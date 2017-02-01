import pickle
import os

# By professor last name
RePEc_codes = { "Ashraf": "pas40", "Bakija": "pba72", "Caprio": "pca519",
                "Chao": "pch1481", "Gentry": "pge25", "Gibson": "pgi275",
                "Godlonton": "pgo596", "Jacobson": "pja277", "Kuttner": "pku75",
                "LaLumia": "pla486", "Leight": "ple706", "Love": "plo157",
                "Montiel": "pmo593", "Nafziger": "pna313", "Olney": "pol130",
                "Pedroni": "ppe635", "Rai": "pra472", "Schmidt": "psc90",
                "Sheppard": "psh80", "Shore-Sheppard": "psh71",
                "Swamy": "psw42", "Watson": "pwa238", "Zimmerman": "pzi72"  }

pickle.dump(RePEc_codes, open("Faculty_Data" + os.sep + "RePEc_codes.p", "wb"), protocol=2)
