# -*- coding: utf-8 -*-
from . import models


def _assign_default_ebook_serial_mail_template(env):
    # On install the template is created after the company column, so the
    # field default could not point to it yet.
    template = env.ref('ebook_serial_delivery.mail_template_ebook_serial', raise_if_not_found=False)
    if template:
        env['res.company'].search([('ebook_serial_mail_template_id', '=', False)]).ebook_serial_mail_template_id = template
