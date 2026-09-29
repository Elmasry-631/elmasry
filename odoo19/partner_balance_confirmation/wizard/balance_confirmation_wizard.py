# -*- coding: utf-8 -*-
import base64
import io
import logging
import os
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime

from lxml import etree

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from ..models.arabic_amount_to_text import amount_to_arabic_text

_logger = logging.getLogger(__name__)


# XML namespaces for Word processing
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = '{%s}' % W_NS


# Placeholders found in the ORIGINAL Word templates (red-colored runs, #EE0000).
# Each entry maps: red placeholder text -> data dict key
# `keep_parens` flag controls whether surrounding parentheses should be
# PRESERVED (True) or STRIPPED (False) when the placeholder is replaced.
# Per user requirement: ONLY the balance value should appear inside `(...)`.
PLACEHOLDERS = {
    'هنا التاريخ المختار': {
        'key': 'confirmation_date',
        'keep_parens': False,
    },
    'هنا اسم العميل': {
        'key': 'partner_name',
        'keep_parens': False,
    },
    'هنا رصيد العميل': {
        'key': 'balance_str',
        'keep_parens': True,   # BALANCE keeps parentheses (per user requirement)
    },
    'اسم موظف القائم بالطباعه': {
        'key': 'printed_by',
        'keep_parens': False,
    },
}

# Sample Arabic amount text embedded in the original templates as examples.
# These need to be replaced with the actual computed amount text.
SAMPLE_AMOUNT_TEXTS = [
    'فقط ستة آلاف وخمسة وثلاثون ريالاً سعودياً لا غير',
    'فقط مائة وعشرون ألفاً وتسعمائة وتسعة وستون ريالاً سعودياً واثنتان وستون هللة لا غير',
    'فقط ستة آلاف وخمسة وثلاثون ريالاً سعودياً و62/100 هللة لا غير',
]


class BalanceConfirmationWizard(models.TransientModel):
    _name = 'balance.confirmation.wizard'
    _description = 'Balance Confirmation Wizard'

    partner_id = fields.Many2one(
        'res.partner', string='Customer', required=True, readonly=True,
        ondelete='cascade',
    )
    confirmation_date = fields.Date(
        string='Confirmation Date', required=True,
        default=fields.Date.context_today,
    )
    template_type = fields.Selection(
        selection=[
            ('amdad', 'Imdad'),
            ('namo', 'Namo'),
        ],
        string='Template', required=True,
        default='amdad',
    )
    notes = fields.Text(string='Additional Notes')
    printed_by = fields.Many2one(
        'res.users', string='Printed By', readonly=True,
        default=lambda self: self.env.user.id,
    )

    # Computed fields (still useful for wizard preview)
    balance = fields.Monetary(
        string='Balance', compute='_compute_balance',
        currency_field='currency_id', store=False,
    )
    balance_text = fields.Char(
        string='Balance in Words', compute='_compute_balance', store=False,
    )
    currency_id = fields.Many2one(
        'res.currency', string='Currency', compute='_compute_balance', store=False,
    )

    @api.depends('partner_id', 'confirmation_date')
    def _compute_balance(self):
        for wiz in self:
            if wiz.partner_id and wiz.confirmation_date:
                balance, currency = wiz.partner_id._get_partner_balance_at_date(
                    wiz.partner_id.id, wiz.confirmation_date,
                )
                wiz.balance = balance
                wiz.currency_id = currency
                wiz.balance_text = amount_to_arabic_text(balance)
            else:
                wiz.balance = 0.0
                wiz.balance_text = amount_to_arabic_text(0.0)
                wiz.currency_id = self.env.company.currency_id

    # ------------------------------------------------------------------
    # Data building
    # ------------------------------------------------------------------
    def _build_report_data(self):
        """Build the data dict with all system-filled values."""
        self.ensure_one()
        self._compute_balance()

        partner_name = self.partner_id.name or ''
        printed_by_name = ''
        if self.printed_by:
            printed_by_name = self.printed_by.name or ''
        if not printed_by_name:
            printed_by_name = self.env.user.name or ''

        confirmation_date_str = ''
        if self.confirmation_date:
            confirmation_date_str = self.confirmation_date.strftime('%Y-%m-%d')

        balance_text = self.balance_text or amount_to_arabic_text(0.0)

        data = {
            'wizard_id': self.id,
            'partner_id': self.partner_id.id,
            'partner_name': partner_name,
            'confirmation_date': confirmation_date_str,
            'template_type': self.template_type or 'amdad',
            'balance': float(self.balance or 0.0),
            'balance_str': '%.2f' % float(self.balance or 0.0),
            'balance_text': balance_text,
            'currency_name': _('Saudi Riyal'),
            'currency_code': 'SAR',
            'printed_by': printed_by_name,
            'notes': self.notes or '',
            'lang': self.env.user.lang,
        }
        _logger.info('Balance confirmation report data: %s', data)
        return data

    # ------------------------------------------------------------------
    # Public actions (called from wizard buttons)
    # ------------------------------------------------------------------
    def action_print_pdf(self):
        """Generate the PDF directly from the original Word template.

        Flow:
          1. Load original .docx template (amdad or namo)
          2. Replace red placeholders with actual values (XML-level, preserves images)
          3. Convert .docx -> PDF via one of:
             a) MS Word COM automation (Windows + MS Word installed) — PREFERRED
             b) LibreOffice headless (any OS)
             c) QWeb rendering (last resort — does NOT match Word 1:1)
          4. Return as download
        """
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_('Please select a customer first.'))
        if not self.confirmation_date:
            raise UserError(_('Please select a confirmation date.'))

        data = self._build_report_data()

        # _generate_pdf_from_word returns a tuple:
        #   (pdf_bytes, used_fallback: bool, fallback_reason: str)
        pdf_bytes, used_fallback, fallback_reason = self._generate_pdf_from_word(data)

        attachment = self.env['ir.attachment'].create({
            'name': _('Balance Confirmation - %s.pdf') % (self.partner_id.name or ''),
            'type': 'binary',
            'datas': base64.b64encode(pdf_bytes).decode(),
            'res_model': 'balance.confirmation.wizard',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        # If we used the QWeb fallback (no Word, no LibreOffice, or both failed),
        # show a warning notification to the user with the download link.
        if used_fallback:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('PDF generated (limited mode)'),
                    'message': fallback_reason or _(
                        'This PDF was rendered using the QWeb fallback and '
                        'will NOT be a 100%% match of the Word template. '
                        'Please check the Odoo log for details.'
                    ),
                    'type': 'warning',
                    'sticky': True,
                    'next': {
                        'type': 'ir.actions.act_url',
                        'url': '/web/content/%s?download=true' % attachment.id,
                        'target': 'self',
                    },
                },
            }

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }

    def action_print_word(self):
        """Export the balance confirmation as a Word (.docx) document.

        Loads the original Word template and fills the red placeholders,
        preserving all images/stamps/logos.
        """
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_('Please select a customer first.'))
        if not self.confirmation_date:
            raise UserError(_('Please select a confirmation date.'))

        data = self._build_report_data()
        docx_bytes = self._generate_docx(data)

        attachment = self.env['ir.attachment'].create({
            'name': _('Balance Confirmation - %s.docx') % (self.partner_id.name or ''),
            'type': 'binary',
            'datas': base64.b64encode(docx_bytes).decode(),
            'res_model': 'balance.confirmation.wizard',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }

    def action_send_email(self):
        """Send the balance confirmation by email to the partner.

        Odoo 19 note: `mail.template.generate_email()` was removed in Odoo 19.
        We use `template.send_mail()` instead, after attaching the generated PDF.
        """
        self.ensure_one()
        if not self.partner_id.email:
            raise UserError(
                _('No email address registered for this customer: %s') % self.partner_id.name
            )

        # 1) Generate the PDF (from Word template)
        data = self._build_report_data()
        pdf_bytes, _used_fb, _fb_reason = self._generate_pdf_from_word(data)

        # 2) Create an attachment for the PDF
        attachment = self.env['ir.attachment'].create({
            'name': _('Balance Confirmation - %s.pdf') % self.partner_id.name,
            'type': 'binary',
            'datas': base64.b64encode(pdf_bytes).decode(),
            'res_model': 'balance.confirmation.wizard',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        # 3) Load the mail template
        template = self.env.ref(
            'partner_balance_confirmation.mail_template_balance_confirmation',
            raise_if_not_found=False,
        )
        if not template:
            raise UserError(_('Email template not found. Please verify the module installation.'))

        # 4) Send the email using Odoo 19 API (send_mail with email_values)
        mail_id = template.send_mail(
            self.id,
            force_send=True,
            email_values={
                'attachment_ids': [(6, 0, [attachment.id])],
            },
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Sent'),
                'message': _('Confirmation has been emailed to customer: %s') % self.partner_id.email,
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    # ------------------------------------------------------------------
    # Word template processing (shared by PDF + Word export)
    # ------------------------------------------------------------------
    def _get_template_path(self, template_type):
        """Return absolute path to the original .docx template."""
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if template_type == 'namo':
            return os.path.join(module_path, 'data', 'template_namo.docx')
        return os.path.join(module_path, 'data', 'template_amdad.docx')

    def _generate_docx(self, data):
        """Load the original Word template and fill placeholders.

        Uses direct XML manipulation (lxml) to preserve all images, stamps,
        and formatting. Falls back to python-docx with safe replacement if
        lxml is not available (shouldn't happen in Odoo 19 - lxml is core).
        """
        template_path = self._get_template_path(data.get('template_type', 'amdad'))
        if not os.path.exists(template_path):
            raise UserError(_('Original Word template not found: %s') % template_path)

        return self._fill_template_safe(template_path, data)

    def _fill_template_safe(self, docx_path, data):
        """SAFE placeholder replacement that preserves ALL images, stamps,
        logos, and text formatting.

        Approach:
          - Work directly on the XML of document.xml using lxml
          - Walk through every <w:t> element (text node) and do string
            replacement on its content
          - Change color from red (#EE0000) to black on modified runs
          - Strip surrounding parentheses ONLY for non-balance placeholders
            (balance keeps its parens per user requirement)
          - This avoids the python-docx bug where setting run.text=''
            destroys <w:drawing> children of the run
        """
        # Build replacement map
        replacements = {}
        for placeholder, info in PLACEHOLDERS.items():
            value = data.get(info['key'], '')
            if value is None:
                value = ''
            replacements[placeholder] = str(value)
        actual_amount_text = data.get('balance_text', '')
        for sample_text in SAMPLE_AMOUNT_TEXTS:
            replacements[sample_text] = actual_amount_text

        # Read the docx as a zip and process document.xml + header/footer XMLs
        output_buf = io.BytesIO()
        with zipfile.ZipFile(docx_path, 'r') as zin:
            with zipfile.ZipFile(output_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    content = zin.read(item.filename)

                    # Process all relevant XML files
                    should_process = (
                        item.filename == 'word/document.xml'
                        or item.filename.startswith('word/header')
                        or item.filename.startswith('word/footer')
                    ) and item.filename.endswith('.xml')

                    if should_process:
                        content = self._replace_placeholders_in_xml(
                            content, replacements
                        )

                    zout.writestr(item, content)

        return output_buf.getvalue()

    def _replace_placeholders_in_xml(self, xml_bytes, replacements):
        """Replace placeholders in a single XML file's content.

        Walks through all <w:t> text elements and does string replacement.
        Changes color from red (#EE0000) to black on modified runs.

        Parentheses policy (per user requirement):
          - For the BALANCE placeholder (`هنا رصيد العميل`): KEEP parentheses
            so the output shows `( 1234.56 )`
          - For all OTHER placeholders (date, customer name, employee name):
            STRIP the surrounding `(` and `)` from adjacent runs so the
            output shows just the value with no parens.
        """
        try:
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.fromstring(xml_bytes, parser)
        except Exception as e:
            _logger.error("Failed to parse XML: %s", e)
            return xml_bytes

        # STEP 1: Do placeholder replacement on <w:t> elements.
        # Track which runs we modified (these hold the filled values).
        # Also track WHICH placeholder each run got (so we know parens policy).
        modified_runs = {}  # id(run_element) -> placeholder_text that was replaced
        filled_count = 0

        for t_elem in tree.iter(W + 't'):
            if t_elem.text is None:
                continue
            original_text = t_elem.text
            new_text = original_text
            matched_placeholder = None
            for placeholder, value in replacements.items():
                if placeholder in new_text:
                    new_text = new_text.replace(placeholder, value)
                    matched_placeholder = placeholder
            if new_text != original_text:
                t_elem.text = new_text
                # Find parent <w:r> for color change + paren cleanup
                parent_r = t_elem.getparent()
                while parent_r is not None and parent_r.tag != W + 'r':
                    parent_r = parent_r.getparent()
                if parent_r is not None:
                    # Determine if this run should keep its parens.
                    # Balance placeholder keeps parens; everything else strips.
                    is_balance = (matched_placeholder == 'هنا رصيد العميل')
                    # Also: the sample amount texts are not "balance", they
                    # are the spelled-out amount; we keep parens for them too
                    # (the original template shows them inside parens).
                    if matched_placeholder in SAMPLE_AMOUNT_TEXTS:
                        keep_parens = True
                    elif matched_placeholder in PLACEHOLDERS:
                        keep_parens = PLACEHOLDERS[matched_placeholder]['keep_parens']
                    else:
                        keep_parens = True
                    modified_runs[id(parent_r)] = {
                        'run': parent_r,
                        'placeholder': matched_placeholder,
                        'keep_parens': keep_parens,
                        'is_balance': is_balance,
                    }
                    filled_count += 1

        # Change color from red to black on modified runs
        for info in modified_runs.values():
            run = info['run']
            rPr = run.find(W + 'rPr')
            if rPr is None:
                rPr = etree.SubElement(run, W + 'rPr')
                run.insert(0, rPr)
            color = rPr.find(W + 'color')
            if color is None:
                color = etree.SubElement(rPr, W + 'color')
            color.set(W + 'val', '000000')

        # STEP 2: Strip surrounding parens for NON-balance placeholders.
        # Case A: placeholder and parens are in the SAME run:
        #   `<w:t>( هنا التاريخ المختار)</w:t>`
        # After replacement this becomes `( 2026-07-10)` — strip the
        # leading `(` and trailing `)` from the run text.
        for info in modified_runs.values():
            if info['keep_parens']:
                continue
            run = info['run']
            t_elems = list(run.iter(W + 't'))
            if not t_elems:
                continue
            run_text = ''.join(t.text or '' for t in t_elems)
            stripped = run_text.strip()
            # Only strip if the entire run text is `( value )` style
            if (stripped.startswith('(') and stripped.endswith(')')
                    and stripped.count('(') == 1 and stripped.count(')') == 1
                    and len(stripped) > 2):
                # Strip leading `(` from the first <w:t> that has it
                for t in t_elems:
                    if t.text and '(' in t.text:
                        t.text = t.text.replace('(', '', 1)
                        break
                # Strip trailing `)` from the last <w:t> that has it
                for t in reversed(t_elems):
                    if t.text and ')' in t.text:
                        idx = t.text.rfind(')')
                        t.text = t.text[:idx] + t.text[idx + 1:]
                        break

        # STEP 3: Strip surrounding parens for NON-balance placeholders.
        # Case B: parens are in SEPARATE adjacent runs (most common case):
        #   Run-prev: `(`
        #   Run-value: `هنا التاريخ المختار` (replaced -> `2026-07-10`)
        #   Run-next:  `)`
        # We walk each paragraph, find modified runs that should NOT keep
        # parens, and strip the `(` / `)` from the immediately adjacent runs.
        for p in tree.iter(W + 'p'):
            runs = list(p.iter(W + 'r'))
            if not runs:
                continue
            for i, run in enumerate(runs):
                info = modified_runs.get(id(run))
                if info is None:
                    continue
                if info['keep_parens']:
                    continue
                # Walk backwards to find the first non-empty preceding run
                for j in range(i - 1, -1, -1):
                    prev_run = runs[j]
                    prev_text = ''.join(t.text or '' for t in prev_run.iter(W + 't'))
                    if not prev_text or prev_text.isspace():
                        continue
                    # If this run's text starts with `(` and the part before is
                    # short (just spaces or empty), strip the `(`.
                    stripped = prev_text.lstrip()
                    if stripped.startswith('('):
                        # Only strip if the `(` is the leading non-space char
                        # AND the run's primary content is the `(` (short).
                        # This avoids stripping legitimate parens deep in text.
                        if len(stripped) <= 4:
                            for t in prev_run.iter(W + 't'):
                                if t.text:
                                    t.text = t.text.replace('(', '', 1)
                    break
                # Walk forwards to find the first non-empty following run
                for j in range(i + 1, len(runs)):
                    next_run = runs[j]
                    next_text = ''.join(t.text or '' for t in next_run.iter(W + 't'))
                    if not next_text or next_text.isspace():
                        continue
                    stripped = next_text.lstrip()
                    if stripped.startswith(')'):
                        if len(stripped) <= 4:
                            for t in next_run.iter(W + 't'):
                                if t.text:
                                    t.text = t.text.replace(')', '', 1)
                    break

        if filled_count > 0:
            _logger.info("Replaced %d placeholder occurrences in XML", filled_count)

        return etree.tostring(
            tree, xml_declaration=True, encoding='UTF-8', standalone=True
        )

    # ------------------------------------------------------------------
    # PDF generation from Word (via LibreOffice headless)
    # ------------------------------------------------------------------
    def _find_libreoffice(self):
        """Find the LibreOffice/soffice executable on Linux or Windows."""
        for name in ('libreoffice', 'soffice', 'soffice.exe', 'libreoffice.exe'):
            path = shutil.which(name)
            if path:
                return path
        if os.name == 'nt':
            win_paths = [
                r'C:\Program Files\LibreOffice\program\soffice.exe',
                r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
                r'D:\Program Files\LibreOffice\program\soffice.exe',
                r'D:\Program Files (x86)\LibreOffice\program\soffice.exe',
                # Chocolatey install path
                r'C:\ProgramData\chocolatey\bin\soffice.exe',
                # Sometimes installed in user-local AppData
                os.path.expandvars(r'%LOCALAPPDATA%\Programs\LibreOffice\program\soffice.exe'),
            ]
            for p in win_paths:
                if p and os.path.exists(p):
                    return p
        else:
            for p in ('/usr/bin/libreoffice', '/usr/bin/soffice',
                      '/usr/lib/libreoffice/program/soffice',
                      '/usr/local/bin/libreoffice',
                      '/snap/bin/libreoffice',
                      '/opt/libreoffice/program/soffice'):
                if os.path.exists(p):
                    return p
        return None

    def _path_to_file_uri(self, path):
        """Convert a filesystem path to a proper `file:` URI.

        On Windows, paths like `C:\\Users\\...` must become
        `file:///C:/Users/...` (THREE slashes, forward slashes).
        On Linux, `/tmp/...` becomes `file:///tmp/...` (THREE slashes).

        Using pathlib.Path.as_uri() handles both cases correctly.
        """
        from pathlib import Path
        try:
            return Path(path).resolve().as_uri()
        except Exception:
            # Manual fallback
            abs_path = os.path.abspath(path)
            if os.name == 'nt':
                # Windows: C:\\Users\\... -> file:///C:/Users/...
                return 'file:///' + abs_path.replace('\\', '/').lstrip('/')
            return 'file://' + abs_path

    def _run_libreoffice_conversion(self, soffice, docx_path, tmpdir):
        """Run LibreOffice headless to convert .docx -> .pdf.

        Tries multiple strategies in order:
          1. With a fresh UserInstallation profile (isolated, concurrent-safe)
          2. Without UserInstallation (in case the profile path itself
             triggers issues — e.g. Windows bootstrap.ini corrupt error)

        Returns the path to the generated PDF, or None if all strategies
        fail.
        """
        outdir = tmpdir
        profile_dir = os.path.join(tmpdir, 'lo_profile')
        try:
            os.makedirs(profile_dir, exist_ok=True)
        except Exception:
            pass

        # Strategy 1: with isolated UserInstallation profile
        cmd_variants = [
            # Variant 1: with UserInstallation (preferred — concurrent-safe)
            [
                soffice,
                '--headless',
                '--nologo',
                '--nofirststartwizard',
                '--norestore',
                '-env:UserInstallation=%s' % self._path_to_file_uri(profile_dir),
                '--convert-to', 'pdf',
                '--outdir', outdir,
                docx_path,
            ],
            # Variant 2: without UserInstallation (fallback — sometimes
            # needed on Windows where the profile path itself can trigger
            # the "bootstrap.ini is corrupt" error)
            [
                soffice,
                '--headless',
                '--nologo',
                '--nofirststartwizard',
                '--norestore',
                '--convert-to', 'pdf',
                '--outdir', outdir,
                docx_path,
            ],
        ]

        last_stderr = b''
        for idx, cmd in enumerate(cmd_variants):
            try:
                _logger.info(
                    "Running LibreOffice (variant %d): %s",
                    idx + 1, ' '.join(cmd),
                )
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    timeout=180,
                    check=False,
                )
                last_stderr = result.stderr or b''
                # Look for the output PDF
                pdf_path = os.path.join(outdir, 'balance_confirmation.pdf')
                if not os.path.exists(pdf_path):
                    pdf_files = [f for f in os.listdir(outdir)
                                 if f.endswith('.pdf') and f != 'balance_confirmation.pdf']
                    if pdf_files:
                        pdf_path = os.path.join(outdir, pdf_files[0])
                if os.path.exists(pdf_path) and result.returncode == 0:
                    _logger.info(
                        "LibreOffice conversion succeeded (variant %d): %s",
                        idx + 1, pdf_path,
                    )
                    return pdf_path
                _logger.warning(
                    "LibreOffice variant %d returned code=%d. stderr=%s",
                    idx + 1, result.returncode,
                    last_stderr.decode('utf-8', errors='replace')[:500],
                )
            except subprocess.TimeoutExpired:
                _logger.warning(
                    "LibreOffice variant %d timed out after 180s", idx + 1
                )
            except Exception as e:
                _logger.warning(
                    "LibreOffice variant %d raised exception: %s", idx + 1, e
                )

        # All variants failed — log the last stderr for debugging
        _logger.error(
            "All LibreOffice conversion variants failed. Last stderr: %s",
            last_stderr.decode('utf-8', errors='replace')[:1000],
        )
        return None, last_stderr

    # ------------------------------------------------------------------
    # Server-side font installation (for LibreOffice PDF conversion)
    # ------------------------------------------------------------------
    # The Word templates use "Sakkal Majalla" for Arabic text.
    #
    # Font priority (so the PDF matches the Word template exactly):
    #   1. The REAL "Sakkal Majalla" font — if the module ships it as
    #      `static/src/fonts/majalla.ttf`, it is installed on the server
    #      and LibreOffice uses it directly (perfect match).
    #   2. The open-source "Amiri" font (visually close) — installed only
    #      as a fallback when the real Sakkal Majalla is not available.
    #
    # The fontconfig alias uses `mode="append"` + `binding="weak"`, so the
    # real Sakkal Majalla is ALWAYS preferred and Amiri is used only when
    # the real font is missing.
    _FONT_INSTALL_LOCK = None

    def _ensure_arabic_fonts_installed(self):
        """Install the Arabic fonts shipped with the module on the server.

        The real Sakkal Majalla font is installed when available (perfect
        Word match); otherwise Amiri is installed as a fallback. A
        fontconfig alias (append/weak) is maintained so the real font
        always wins when present.

        Idempotent: skips installation if the fonts are already registered
        with fontconfig. Safe to call on every PDF generation.
        """
        import threading
        if BalanceConfirmationWizard._FONT_INSTALL_LOCK is None:
            BalanceConfirmationWizard._FONT_INSTALL_LOCK = threading.Lock()

        # Quick check: is the real Sakkal Majalla already visible to
        # fontconfig (real font file, not the Amiri alias fallback)?
        if self._is_sakkal_majalla_installed():
            # Still make sure the fallback alias exists (cheap).
            self._ensure_sakkal_majalla_alias()
            return True

        with BalanceConfirmationWizard._FONT_INSTALL_LOCK:
            # Re-check inside the lock
            if self._is_sakkal_majalla_installed():
                self._ensure_sakkal_majalla_alias()
                return True

            _logger.info(
                "Sakkal Majalla font not detected on server. Installing "
                "fonts from module static/src/fonts/..."
            )
            try:
                self._install_fonts_from_module()
                self._ensure_sakkal_majalla_alias()
                self._refresh_font_cache()
                if self._is_sakkal_majalla_installed():
                    _logger.info(
                        "Sakkal Majalla font installed successfully. "
                        "PDF will match the Word template exactly."
                    )
                    return True
                if self._is_font_installed('Amiri'):
                    _logger.warning(
                        "Real Sakkal Majalla font not found in module; "
                        "installed Amiri fallback instead. PDF Arabic text "
                        "will use Amiri (close but not an exact match)."
                    )
                    return True
                _logger.error(
                    "No Arabic font (Sakkal Majalla or Amiri) is visible "
                    "to fontconfig. PDF Arabic text may not render."
                )
                return False
            except Exception as e:
                _logger.warning(
                    "Failed to install Arabic fonts on server: %s. "
                    "PDF Arabic text may not render correctly.", e,
                    exc_info=True,
                )
                return False

    def _is_sakkal_majalla_installed(self):
        """Check whether the REAL Sakkal Majalla font (not the Amiri alias
        fallback) is visible to fontconfig."""
        try:
            result = subprocess.run(
                ['fc-match', 'Sakkal Majalla'],
                capture_output=True, timeout=10,
            )
            # The real font file is majalla.ttf; the fallback resolves to
            # Amiri-Regular.ttf. Distinguish by the file name.
            return b'majalla' in result.stdout.lower()
        except Exception:
            return False

    def _is_font_installed(self, family):
        """Check whether fontconfig can see a font family."""
        try:
            result = subprocess.run(
                ['fc-list', ':family=%s' % family],
                capture_output=True, timeout=10,
            )
            return family.encode() in result.stdout
        except Exception:
            return False

    def _get_font_install_dir(self):
        """Return the best writable system font directory.

        Preference order:
          1. /usr/share/fonts/truetype/arabic  (system-wide, persistent)
          2. /usr/local/share/fonts            (system-wide fallback)
          3. ~/.fonts                          (user-local fallback)
        """
        candidates = [
            '/usr/share/fonts/truetype/arabic',
            '/usr/local/share/fonts',
        ]
        for path in candidates:
            try:
                os.makedirs(path, exist_ok=True)
                # Test writability
                test_file = os.path.join(path, '.write_test')
                with open(test_file, 'w') as f:
                    f.write('ok')
                os.remove(test_file)
                return path
            except (OSError, PermissionError):
                continue
        # Last resort: user-local fonts
        home_fonts = os.path.join(os.path.expanduser('~'), '.fonts')
        os.makedirs(home_fonts, exist_ok=True)
        return home_fonts

    def _install_fonts_from_module(self):
        """Copy all font files (.ttf/.otf) shipped with the module's
        static/src/fonts/ directory into the system font directory.

        This installs the real Sakkal Majalla (majalla.ttf) when present,
        plus the Amiri fallback fonts.
        """
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_dir = os.path.join(module_path, 'static', 'src', 'fonts')
        if not os.path.isdir(src_dir):
            _logger.warning("Module font directory not found: %s", src_dir)
            return

        dest_dir = self._get_font_install_dir()
        installed = 0
        for fname in sorted(os.listdir(src_dir)):
            if not fname.lower().endswith(('.ttf', '.otf')):
                continue
            src = os.path.join(src_dir, fname)
            dest = os.path.join(dest_dir, fname)
            if not os.path.exists(src):
                continue
            if os.path.exists(dest):
                # Compare sizes; skip if identical
                if os.path.getsize(src) == os.path.getsize(dest):
                    _logger.info("Font already present (same size): %s", dest)
                    installed += 1
                    continue
            try:
                shutil.copy2(src, dest)
                _logger.info("Installed font: %s -> %s", src, dest)
                installed += 1
            except Exception as e:
                _logger.warning("Failed to copy %s: %s", src, e)
        if installed == 0:
            _logger.warning("No fonts installed from module fonts dir: %s", src_dir)

    def _ensure_sakkal_majalla_alias(self):
        """Create a fontconfig fallback alias Sakkal Majalla -> Amiri.

        Uses `mode="append"` + `binding="weak"` so the REAL Sakkal Majalla
        font is always tried first (when installed on the server) and Amiri
        is used ONLY as a fallback when the real font is missing. This way
        the PDF matches the Word template exactly when the real font exists.
        """
        alias_content = """<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <!--
    Fallback alias: "Sakkal Majalla" (Microsoft commercial Arabic font used
    in the Word templates) -> "Amiri" (open-source Arabic font bundled with
    this Odoo module).

    IMPORTANT: This uses mode="append" + binding="weak" so fontconfig
    TRIES the real Sakkal Majalla font FIRST (if installed on the server)
    and only falls back to Amiri when the real font is missing. This way
    the PDF matches the Word template exactly when the real font exists.
  -->
  <match target="pattern">
    <test name="family"><string>Sakkal Majalla</string></test>
    <edit name="family" mode="append" binding="weak"><string>Amiri</string></edit>
  </match>
</fontconfig>
"""

        # Try system-wide fontconfig first, fall back to user-local
        targets = [
            '/etc/fonts/conf.d/99-sakkal-majalla-alias.conf',
            os.path.join(
                os.path.expanduser('~'), '.config', 'fontconfig',
                'conf.d', '99-sakkal-majalla-alias.conf',
            ),
        ]
        for target in targets:
            try:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                # Skip if already present with same content
                if os.path.exists(target):
                    with open(target, 'r') as f:
                        if f.read().strip() == alias_content.strip():
                            return
                with open(target, 'w') as f:
                    f.write(alias_content)
                _logger.info("Sakkal Majalla alias installed: %s", target)
                return
            except (OSError, PermissionError) as e:
                _logger.warning(
                    "Cannot write fontconfig alias to %s: %s", target, e,
                )
                continue

    def _refresh_font_cache(self):
        """Run `fc-cache -f` to refresh fontconfig cache."""
        try:
            subprocess.run(
                ['fc-cache', '-f'],
                capture_output=True, timeout=60,
            )
            _logger.info("Font cache refreshed (fc-cache -f).")
        except subprocess.TimeoutExpired:
            _logger.warning("fc-cache timed out.")
        except Exception as e:
            _logger.warning("fc-cache failed: %s", e)

    def _generate_pdf_from_word(self, data):
        """Generate a PDF from the filled Word template.

        Conversion pipeline (tried in order):
          1. MS Word COM automation  — Windows + MS Word installed (BEST match)
          2. LibreOffice headless     — any OS, requires LibreOffice install
                                       (the real Sakkal Majalla font is
                                        auto-installed from the module so the
                                        PDF matches the Word template exactly)
          3. QWeb rendering           — last resort, does NOT match Word 1:1

        Returns:
            tuple: (pdf_bytes: bytes, used_fallback: bool, fallback_reason: str)
                - pdf_bytes: the generated PDF content
                - used_fallback: True if QWeb was used (PDF won't match Word 1:1)
                - fallback_reason: user-facing message explaining the fallback
        """
        # Step 0: ensure the Arabic font (Amiri) is installed on the server
        # and aliased to Sakkal Majalla so LibreOffice can render Arabic.
        # This is idempotent and cheap if already installed.
        self._ensure_arabic_fonts_installed()

        # Step 1: generate the filled .docx (with all images preserved)
        docx_bytes = self._generate_docx(data)

        tmpdir = tempfile.mkdtemp(prefix='balance_conf_')
        try:
            docx_path = os.path.join(tmpdir, 'balance_confirmation.docx')
            with open(docx_path, 'wb') as f:
                f.write(docx_bytes)

            # ---- Strategy 1: MS Word COM automation (Windows only) ----
            word_pdf = self._try_convert_with_msword(docx_path, tmpdir)
            if word_pdf is not None:
                _logger.info("PDF generated via MS Word COM automation.")
                return self._set_pdf_metadata(word_pdf, data), False, ''

            # ---- Strategy 2: LibreOffice headless ----
            soffice = self._find_libreoffice()
            if soffice:
                lo_result = self._run_libreoffice_conversion(
                    soffice, docx_path, tmpdir
                )
                # _run_libreoffice_conversion returns either a path (str)
                # or a (None, stderr_bytes) tuple on failure.
                if isinstance(lo_result, str):
                    pdf_path = lo_result
                    with open(pdf_path, 'rb') as f:
                        pdf_bytes = f.read()
                    _logger.info("PDF generated via LibreOffice.")
                    return self._set_pdf_metadata(pdf_bytes, data), False, ''
                # LibreOffice failed — log diagnostic
                _unused, last_stderr = lo_result
                stderr_text = last_stderr.decode('utf-8', errors='replace')
                diagnostic = self._build_libreoffice_diagnostic(stderr_text)
                _logger.error("LibreOffice conversion failed. Diagnostic:\n%s",
                              diagnostic)
            else:
                stderr_text = ''
                _logger.warning("LibreOffice not found on the server.")

            # ---- Strategy 3: QWeb fallback ----
            # Build a user-facing message based on what we know.
            fallback_reason = self._build_fallback_reason(stderr_text)
            _logger.warning(
                "Falling back to QWeb PDF rendering. Reason:\n%s",
                fallback_reason,
            )
            pdf_bytes = self._generate_pdf_qweb_fallback(data)
            return self._set_pdf_metadata(pdf_bytes, data), True, fallback_reason

        finally:
            try:
                shutil.rmtree(tmpdir)
            except Exception:
                pass

    def _try_convert_with_msword(self, docx_path, outdir):
        """Attempt to convert .docx -> .pdf using MS Word COM automation.

        This works ONLY on Windows with Microsoft Word installed. It uses
        the real MS Word application to perform the conversion, so the
        resulting PDF is a 100% match of the Word template.

        Returns:
            bytes: the PDF content, or None if conversion failed / not available.
        """
        if os.name != 'nt':
            return None  # MS Word COM only works on Windows

        try:
            import win32com.client  # type: ignore
            import pythoncom  # type: ignore
        except ImportError:
            _logger.info(
                "pywin32 not installed. MS Word COM automation skipped. "
                "Install with: pip install pywin32"
            )
            return None

        word_app = None
        doc = None
        try:
            # Initialize COM for this thread
            pythoncom.CoInitialize()
            # Create a Word.Application instance
            word_app = win32com.client.DispatchEx('Word.Application')
            word_app.Visible = False
            word_app.DisplayAlerts = False

            # Open the document (absolute path required)
            docx_abs = os.path.abspath(docx_path)
            pdf_abs = os.path.abspath(
                os.path.join(outdir, 'balance_confirmation.pdf')
            )

            _logger.info(
                "MS Word COM: opening %s", docx_abs,
            )
            doc = word_app.Documents.Open(docx_abs, ReadOnly=True)

            # ExportAsFixedFormat: 17 = wdExportFormatPDF
            # https://learn.microsoft.com/en-us/office/vba/api/word.document.exportasfixedformat
            doc.ExportAsFixedFormat(
                OutputFileName=pdf_abs,
                ExportFormat=17,            # wdExportFormatPDF
                OpenAfterExport=False,
                OptimizeFor=0,              # wdExportOptimizeForPrint
                Range=0,                    # wdExportAllDocument
                Item=0,                     # wdExportDocumentContent
                IncludeDocProps=True,
                KeepIRM=True,
                CreateBookmarks=1,          # wdExportCreateHeadingBookmarks
                DocStructureTags=True,
                BitmapMissingFonts=True,
                UseISO19005_1=False,
            )

            if not os.path.exists(pdf_abs):
                _logger.error(
                    "MS Word COM: PDF file not created at %s", pdf_abs,
                )
                return None

            with open(pdf_abs, 'rb') as f:
                return f.read()

        except Exception as e:
            _logger.warning(
                "MS Word COM automation failed: %s", e, exc_info=True,
            )
            return None
        finally:
            # Always close the document and quit Word, even on error
            try:
                if doc is not None:
                    doc.Close(SaveChanges=False)
            except Exception:
                pass
            try:
                if word_app is not None:
                    word_app.Quit()
            except Exception:
                pass
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass

    def _build_fallback_reason(self, libreoffice_stderr):
        """Build a user-facing message explaining why we fell back to QWeb.

        Provides actionable guidance based on what failed.
        """
        if not libreoffice_stderr:
            # No LibreOffice available + no MS Word
            return _(
                'Neither MS Word nor LibreOffice is available on the '
                'server, so this PDF was rendered using the QWeb fallback '
                'and will NOT be a 100%% match of the Word template.\n\n'
                'For an exact match, install ONE of:\n\n'
                'Option A — Microsoft Word (Windows only, BEST match):\n'
                '  1. Install MS Office (Word) on the server.\n'
                '  2. Install pywin32: pip install pywin32\n'
                '  3. Restart Odoo.\n\n'
                'Option B — LibreOffice (any OS):\n'
                '  - Linux: apt-get install -y libreoffice\n'
                '         or yum install -y libreoffice\n'
                '  - Windows: download from '
                'https://www.libreoffice.org/download/'
            )

        stderr_lower = libreoffice_stderr.lower()
        if 'bootstrap.ini' in stderr_lower or 'corrupt' in stderr_lower:
            return _(
                'LibreOffice installation appears to be corrupt '
                '(bootstrap.ini error).\n\n'
                'Two options to fix:\n\n'
                'Option A — Use Microsoft Word instead (RECOMMENDED on '
                'Windows):\n'
                '  1. Install MS Office (Word) on the server.\n'
                '  2. Install pywin32: pip install pywin32\n'
                '  3. Restart Odoo.\n'
                '(No need to uninstall LibreOffice — Word takes priority)\n\n'
                'Option B — Repair LibreOffice:\n'
                '  1. Close any running LibreOffice processes.\n'
                '  2. Delete the LibreOffice user profile folder:\n'
                '       %APPDATA%\\LibreOffice\n'
                '  3. Repair the installation:\n'
                '       Control Panel → Programs → LibreOffice → '
                'Change → Repair\n'
                '  4. If repair fails, uninstall LibreOffice, then '
                'reinstall as Administrator from:\n'
                '       https://www.libreoffice.org/download/\n'
                '  5. Run LibreOffice once manually (GUI) to initialize '
                'the profile.\n'
                '  6. Restart Odoo.\n\n'
                'The PDF was generated using the QWeb fallback and will '
                'NOT be a 100%% match of the Word template.'
            )
        if 'permission' in stderr_lower or 'access' in stderr_lower:
            return _(
                'LibreOffice failed due to a permission issue.\n\n'
                'Troubleshooting:\n'
                '  - Make sure the Odoo service user has read access to '
                'soffice.exe\n'
                '  - Make sure the Odoo service user has write access to '
                'the TEMP folder\n'
                '  - On Windows, run Odoo as a user with normal desktop '
                'permissions.\n\n'
                'Alternatively, install MS Word + pywin32 to use MS Word '
                'COM automation instead.\n\n'
                'The PDF was generated using the QWeb fallback and will '
                'NOT be a 100%% match of the Word template.'
            )
        return _(
            'Both MS Word COM and LibreOffice failed to convert Word to '
            'PDF.\n\n'
            'LibreOffice STDERR: %s\n\n'
            'Troubleshooting:\n'
            '  - Install MS Office (Word) + pywin32 on the server, OR\n'
            '  - Repair/reinstall LibreOffice.\n\n'
            'The PDF was generated using the QWeb fallback and will NOT '
            'be a 100%% match of the Word template. Check the Odoo log '
            'for more details.'
        ) % libreoffice_stderr[:300]

    def _build_libreoffice_diagnostic(self, stderr_text):
        """Build a human-readable diagnostic message for LibreOffice
        failures, including OS-specific troubleshooting steps.
        """
        stderr_lower = stderr_text.lower()
        lines = [
            "LibreOffice failed to convert Word to PDF.",
            "",
            "STDERR: %s" % stderr_text[:500],
            "",
        ]

        if 'bootstrap.ini' in stderr_lower or 'corrupt' in stderr_lower:
            lines.extend([
                "Detected issue: LibreOffice installation/profile is corrupt.",
                "",
                "Troubleshooting steps (Windows):",
                "  1. Close any running LibreOffice processes (Task Manager).",
                "  2. Delete the LibreOffice user profile folder:",
                "       %APPDATA%\\LibreOffice",
                "  3. Repair the installation:",
                "       Control Panel → Programs → LibreOffice → Change → Repair",
                "  4. If repair fails, uninstall LibreOffice completely,",
                "     then reinstall as Administrator:",
                "       https://www.libreoffice.org/download/",
                "  5. After reinstall, run LibreOffice once manually (GUI)",
                "     to initialize the profile, then restart Odoo.",
                "",
            ])
        elif 'permission' in stderr_lower or 'access' in stderr_lower:
            lines.extend([
                "Detected issue: Permission denied.",
                "",
                "Troubleshooting:",
                "  - Make sure the Odoo service user has read access to",
                "    'C:\\Program Files\\LibreOffice\\program\\soffice.exe'",
                "  - Make sure the Odoo service user has write access to",
                "    the Windows TEMP folder.",
                "  - On Windows, run the Odoo service as a user with normal",
                "    desktop permissions (not LocalSystem).",
                "",
            ])
        else:
            lines.extend([
                "Troubleshooting steps:",
                "  1. Verify LibreOffice runs manually:",
                "       soffice --headless --convert-to pdf test.docx",
                "  2. Restart the Odoo service.",
                "  3. Check the Odoo log for more details.",
                "",
            ])

        return '\n'.join(lines)

    def _generate_pdf_qweb_fallback(self, data):
        """Fallback: render the PDF using the QWeb template.

        Used when:
          - LibreOffice is not installed, OR
          - LibreOffice fails to convert (e.g. corrupt installation)
        """
        report_action = self.env.ref(
            'partner_balance_confirmation.action_report_balance_confirmation'
        )
        pdf_content, _ext = self.env['ir.actions.report']._render_qweb_pdf(
            report_action.report_name,
            res_ids=self.ids,
            data=data,
        )
        return pdf_content

    def _set_pdf_metadata(self, pdf_bytes, data):
        """Set clean PDF metadata so the file doesn't expose the toolchain.

        Replaces any inherited metadata (e.g. 'python-docx' author, 'LibreOffice'
        producer) with proper business metadata. Falls back to returning the
        original bytes if pypdf is not available or fails.
        """
        try:
            from pypdf import PdfReader, PdfWriter
        except ImportError:
            try:
                from PyPDF2 import PdfReader, PdfWriter  # type: ignore
            except ImportError:
                return pdf_bytes  # No pypdf available — return as-is

        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            partner_name = data.get('partner_name', '') or ''
            confirmation_date = data.get('confirmation_date', '') or ''
            template_type = data.get('template_type', 'amdad') or 'amdad'
            template_label = 'Imdad' if template_type == 'amdad' else 'Namo'

            writer.add_metadata({
                '/Title': 'Balance Confirmation - %s' % partner_name,
                '/Author': 'Balance Confirmation Module',
                '/Subject': 'Customer Balance Confirmation (%s template) - %s' % (
                    template_label, confirmation_date,
                ),
                '/Keywords': 'Balance Confirmation, Customer Statement, %s' % template_label,
                '/Creator': 'Balance Confirmation Module (Odoo 19)',
                '/Producer': 'Balance Confirmation Module',
            })

            out_buf = io.BytesIO()
            writer.write(out_buf)
            return out_buf.getvalue()
        except Exception as e:
            _logger.warning("Failed to set PDF metadata: %s", e)
            return pdf_bytes  # Return original on any failure
