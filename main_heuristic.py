from Instance import *
from Extract import *


if __name__ == "__main__":

    extracted = Extract("instance_one/dados_trab_2_10_struc_01")
    instance = Instance(extracted.get_M(),
                        extracted.get_T(), 
                        extracted.get_S())
    instance.to_string()
