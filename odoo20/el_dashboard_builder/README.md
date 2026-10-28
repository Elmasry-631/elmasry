# Dashboard Builder for Odoo 20 Enterprise

A powerful, user-friendly dashboard builder module that allows users to create custom dashboards with drag-and-drop widgets.

## Features

### Dashboard Designer
- **Visual Drag-and-Drop Editor**: Intuitive grid-based layout editor with 12-column responsive grid
- **Real-time Preview**: See changes instantly as you build
- **Responsive Design**: Automatic layout adjustment for different screen sizes
- **Widget Locking**: Prevent accidental movement of critical widgets
- **Visibility Control**: Show/hide widgets without deleting them

### Built-in Widgets

| Category | Widgets |
|----------|---------|
| **KPI / Metrics** | KPI Card, KPI Card Grouped |
| **Charts** | Bar Chart, Line Chart, Pie/Donut Chart |
| **Tables** | Data Table, Pivot Table |
| **Gauges** | Gauge/Speedometer, Progress Bar |
| **Custom** | HTML/Markdown Widget |
| **Actions** | Action Buttons |
| **Calendar** | Calendar View |

### Dashboard Management
- **Sharing**: Public links, embed codes, user/group permissions
- **Favorites**: Mark dashboards as favorites for quick access
- **Tags**: Organize dashboards with custom tags
- **Export**: PDF, Excel, and JSON export
- **Duplication**: Clone dashboards with all widgets
- **Multi-company**: Full multi-company support

### Security & Permissions
- **Role-based Access**: User, Manager, Administrator roles
- **Record Rules**: Users see only their own dashboards (unless public)
- **Widget-level Permissions**: Control who can create/edit widgets

## Installation

1. Copy the `el_dashboard_builder` folder to your Odoo addons path
2. Update the Apps list
3. Search for "Dashboard Builder" and click Install

## Usage

### Creating a Dashboard
1. Go to **Dashboard Builder → My Dashboards**
2. Click **Create** to make a new dashboard
3. Enter dashboard name, description, and configure grid settings
4. Click **Edit Layout** to open the visual editor

### Adding Widgets
1. In the editor, drag widgets from the left sidebar onto the grid
2. Click the gear icon on any widget to configure it
3. Resize widgets by dragging the bottom-right corner
4. Reposition by dragging the widget header

### Configuring Widgets
Each widget type has specific configuration options:

**KPI Card**
- Model, Field, Aggregation (sum, avg, count, min, max)
- Domain filters, Label, Prefix/Suffix
- Trend comparison, Target values
- Color thresholds

**Charts**
- Model, X/Y Fields, Aggregation
- Group by field for series
- Time granularity (for line charts)
- Colors, Legends, Data labels

**Tables**
- Model, Fields to display
- Column formatting (currency, percentage, date, etc.)
- Sorting, Pagination, Search

### Sharing Dashboards
1. Open a dashboard and go to the **Sharing** tab
2. Create a share link with optional password and expiry
3. Copy the embed code for iframe integration
4. Manage user/group access permissions

## Technical Details

### Models
- `dashboard.builder` - Main dashboard model
- `dashboard.builder.item` - Dashboard items/widgets
- `dashboard.builder.widget` - Widget definitions
- `dashboard.builder.share` - Sharing configurations
- `dashboard.builder.tag` - Dashboard tags

### Architecture
- **Backend**: Python models with ORM, JSON configuration storage
- **Frontend**: Owl components, GridStack.js for drag-and-drop
- **Charts**: Chart.js for all chart widgets
- **Styling**: SCSS with Bootstrap 5 variables

### API Endpoints
- `GET /dashboard/builder/<id>` - View dashboard
- `GET /dashboard/builder/<id>/edit` - Edit dashboard
- `GET /dashboard/builder/shared/<token>` - Shared dashboard
- `POST /dashboard/builder/api/items/reorder` - Save positions
- `POST /dashboard/builder/api/items/<id>/configure` - Save widget config
- `GET /dashboard/builder/api/items/<id>/data` - Fetch widget data

## Customization

### Adding Custom Widgets
1. Create a new widget record in **Widget Library**
2. Define the component name, schema, and default config
3. Create the Owl component in `static/src/js/widgets/`
4. Register the component: `window.DashboardMyWidget = MyWidgetComponent`

### Extending Dashboard Model
```python
class MyDashboard(models.Model):
    _inherit = 'dashboard.builder'
    
    my_custom_field = fields.Char()
```

## Requirements
- Odoo 20.0 (Community or Enterprise)
- `web`, `web_editor`, `base_setup` modules

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License
LGPL-3

## Author
Elmasry - https://github.com/Elmasry-631

## Changelog

### 20.0.1.0.0 (2026)
- Initial release
- 12 built-in widget types
- Drag-and-drop editor with GridStack
- Chart.js integration
- Sharing and embedding
- PDF/Excel/JSON export
- Multi-company and RTL support