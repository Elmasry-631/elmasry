# -*- coding: utf-8 -*-


def migrate(cr, version):
    """Detach stored redirect view references before Odoo refreshes QWeb views.

    Older module revisions stored ``payment_provider.redirect_form_view_id`` as a
    hard foreign key to this module's QWeb template. During upgrade, Odoo can
    refresh or replace the template records, which leads PostgreSQL to reject
    the delete while the provider row still points to the old view.

    The provider now resolves its redirect view dynamically through
    ``_get_redirect_form_view()``, so clearing the stored FK is safe and keeps
    existing databases upgradeable.
    """

    cr.execute(
        """
        UPDATE payment_provider
           SET redirect_form_view_id = NULL
         WHERE code = 'alrajhi_arb'
           AND redirect_form_view_id IS NOT NULL
        """
    )
