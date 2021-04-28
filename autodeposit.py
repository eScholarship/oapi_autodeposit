########################################
#
#   Entry point for auto-deposit
#
########################################
from controlIntf import controller
from depositFields import units

print("Starting autodeposit")

x = controller()

# obtain pubIds for autdeposit
# perform deposits in batches

x.performDeposits()
#x.getEscholSeries()
print("Completed autodeposit of " + str(x.depositCount))
