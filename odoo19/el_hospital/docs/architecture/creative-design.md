# Creative Design — el_hospital

## 5 Creative Lenses Applied

### Lens 1: Pattern Discovery (Odoo Design Patterns)
- **Master-Detail**: patient (master) ↔ allergies, diseases, appointments, records
- **Document Workflow**: appointment, admission, lab.test, radiology (state machines)
- **Resource Utilization**: beds ↔ wards (occupancy tracking)
- **Sequence Document**: all operational models have sequence codes
- **Smart Button Hub**: patient form (appointment_count, admission_count)

### Lens 2: UX Innovation
- **Kanban for physicians**: card-based with photo + specialization + patient count
- **Calendar for appointments**: visual scheduling, color by physician
- **Color-coded states**: badge widgets with semantic colors (green=done, red=cancelled)
- **Smart buttons on patient**: one-click navigation to related records
- **Bed status badges**: instant visual of ward occupancy

### Lens 3: Smart Automation
- **Auto-create medical record** when appointment is marked done
- **Auto-reserve bed** on admission (bed.state = occupied)
- **Auto-free bed** on discharge
- **Auto-link** prescription/lab/radiology to medical record
- **Email notifications**: appointment confirmation, lab results ready, discharge summary

### Lens 4: Future-Proofing
- **Abstract base for medical documents** (could add dental, physiotherapy later)
- **Extensible bed model** (could add ICU equipment tracking)
- **Insurance-ready billing** (line-level service types allow insurance mapping)
- **Multi-company ready** (company_id on all models)

### Lens 5: Wow Factor
- **Executive dashboard**: bed occupancy gauge, revenue chart, today's appointments
- **Patient 360° view**: all medical data on one form (EMR + prescriptions + labs + radiology)
- **One-click prescription from medical record**
- **Printable prescription** with professional hospital layout
- **Color-coded wards** with live occupancy stats

## Color Palette (Dashboard)
Following the Elmasry signature dashboard design system:
- Navy: `#1B2A4E` (primary background)
- Amber: `#F5A623` (KPI accent stripe)
- White cards on navy
- Status colors: green `#28a745`, blue `#17a2b8`, red `#dc3545`, grey `#6c757d`
