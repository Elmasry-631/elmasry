# Transaction Tracker Module

## Overview

**Transaction Tracker** is an Odoo 19 module that automatically logs every Create, Write, and Unlink operation performed by users across all installed Odoo models. It provides full audit trail capabilities with dashboards, reports, and configurable per-model tracking settings.

## Features

- **Automatic Tracking**: Hooks into Odoo's base model to capture every CRUD operation across all modules
- **Per-Model Configuration**: Enable or disable tracking for specific models and operation types
- **Dashboard & Analytics**: Pivot tables, graphs, and kanban views for activity analysis
- **PDF Reports**: Professional report templates for audit documentation
- **Suspicious Activity Detection**: Automatically flags bulk operations (bulk delete, bulk write)
- **IP Address Logging**: Records the IP address of the user performing each operation
- **Old/New Value Tracking**: Captures before/after snapshots for write operations
- **Immutable Logs**: Transaction logs cannot be modified or deleted after creation
- **Security**: Role-based access with Manager (full) and User (own logs only) levels

## Installation

1. Upload the `transaction_tracker.zip` file to your Odoo instance
2. Go to **Apps → Upload Module**
3. Install the module
4. Go to **Transaction Tracker → Configuration → Tracker Settings**
5. Click **Auto-Populate Models** to create tracking configurations for all installed models

## Configuration

### Tracker Settings

Navigate to **Transaction Tracker → Configuration → Tracker Settings** to configure which models and operations to track.

For each model you can:
- **Track Create**: Log when new records are created
- **Track Write**: Log when records are modified (captures changed fields + old/new values)
- **Track Delete**: Log when records are deleted (captures snapshot before deletion)
- **Track Read**: Log when records are viewed (disabled by default due to high volume)

### Security Groups

| Group | Access Level |
|-------|-------------|
| Transaction Tracker / Manager | Full access to all logs, configuration, and reports |
| Transaction Tracker / User | Read-only access to own activity logs |

## Usage

### Viewing Logs

Go to **Transaction Tracker → Transaction Logs** to view all tracked operations. Use filters and group-by options to analyze activity:
- Filter by operation type (Create/Write/Delete/Read)
- Filter by time period (Today/This Week/This Month)
- Filter by suspicious activity
- Group by User, Model, Operation, Date, or Module

### Dashboard

Go to **Transaction Tracker → Dashboard** for visual analytics with pivot tables and graphs showing activity trends.

### Reports

Select one or more transaction logs and use the print menu to generate a PDF report.

## Technical Details

### Models

| Model | Description |
|-------|-------------|
| `transaction.log` | Stores all tracked operations (immutable) |
| `transaction.tracker.config` | Per-model tracking configuration |

### How It Works

The module inherits the `base` abstract model and overrides `create()`, `write()`, and `unlink()` methods. Each operation is logged to `transaction.log` with:
- User who performed the operation
- Model and record ID affected
- Operation type (create/write/unlink)
- Before/after values (JSON)
- IP address
- Suspicious activity flag

### Infinite Recursion Protection

- Context flag `skip_transaction_tracking=True` prevents the logger from logging itself
- Internal models (`ir.*`, `base.*`, `mail.*`, `bus.*`) are excluded from tracking
- Module install/upgrade operations are excluded
- Tracker config and log models are excluded

## Author

**Ibrahim Elmasry** — Senior Odoo Developer + DevOps + Implementation Consultant

## License

LGPL-3
