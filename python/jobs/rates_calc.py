"""
numbers based on https://www.wko.at/service/arbeitsrecht-sozialrecht/Neue_Selbststaendige_einfach.html

NOTE: base earning should be higher since there is no 13th salary...
"""

# absolute
MAX_BASE_EARNING = 6615

# percentage
HEALTH_INSURANCE = 6.80

# percentage
PENSION_INSURANCE = 18.5

# percentage
SELF_EMPLOYED_PROVISION = 1.53

# absolute
ACCIDENT_INSURANCE = 10.64

# move this to a func
earning = MAX_BASE_EARNING

hin = (earning/100)*HEALTH_INSURANCE
pin = (earning/100)*PENSION_INSURANCE
sep = (earning/100)*SELF_EMPLOYED_PROVISION

commission = hin+pin+sep+ACCIDENT_INSURANCE

print(f"{commission:.2f}")
