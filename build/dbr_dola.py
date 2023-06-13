from build.dbr_inv import dbr_per_inv
from build.inv_fx import inv_fx

def dbr_dola():
  dbr_inv_data = dbr_per_inv()
  dbr_per = dbr_inv_data['dbr_per_inv']
  
  inv_fx_data = inv_fx()
  fx = inv_fx_data['inv_fx']

  dbr_dola = dbr_per / fx
  
  return {"dbr_dola": dbr_dola}