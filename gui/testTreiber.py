from WrapperEMRFeldsonde import WrapperEMRFeldsonde
import time
import cProfile

instWrapperEMR = WrapperEMRFeldsonde("ASRL3::INSTR") # Adresse als Variable von GUI übernehmen

instWrapperEMR.readval()
