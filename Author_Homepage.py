import pickle
import os

# By professor last name
Author_Homepage = { "Ashraf": "qha1", "Bakija": "jbakija", "Bolton": "rbolton",
                    "Bradburd": "rbradbur", "Caprio": "gcaprio", "Chao": "mc20",
                    "Fortunato": "mfortuna", "Gentry": "wgentry", "Gibson": "mg17",
                    "Godlonton": "sg5", "Jacobson": "saj2", "Kuttner": "knk1",
                    "LaLumia": "sl2", "Leight": "jl14", "Love": "dlove",
                    "Montiel": "pmontiel", "Nafziger": "snafzige", "Olney": "wwo1",
                    "Pedroni": "ppedroni", "Phelan": "gp4", "Rai": "arai",
                    "Schmidt": "lschmidt", "Sheppard": "ssheppar",
                    "Shore-Sheppard": "lshore", "Swamy": "aswamy",
                    "Watson": "twatson", "Zimmerman": "dzimmerm"  }

pickle.dump(Author_Homepage, open("Faculty_Data" + os.sep + "Author_Homepage.p", "wb"), protocol=2)
