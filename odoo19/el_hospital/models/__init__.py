"""Models package for el_hospital.

Import order matters: parent/master models first, then models that depend on them.
"""

from . import hospital_department
from . import hospital_physician
from . import hospital_patient
from . import hospital_appointment
from . import hospital_medical_record
from . import hospital_prescription
from . import hospital_ward
from . import hospital_bed
from . import hospital_admission
from . import hospital_lab_test
from . import hospital_radiology
from . import hospital_medicament
from . import hospital_billing
from . import hospital_dashboard
