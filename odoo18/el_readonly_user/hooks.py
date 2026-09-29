# -*- coding: utf-8 -*-


_READONLY_WRITABLE_MODELS = {
    'res.users.log', 'mail.channel', 'mail.alias',
    'bus.presence', 'res.lang', 'mail.channel.member',
    'bus.bus', 'mail.message', 'mail.followers',
}

# Some Odoo stock forms and workflows perform permission checks for write access
# while rendering/processing a record. Granting the ACL-level write capability
# keeps those checks from failing; the readonly record-rule layer below still
# blocks every actual write/create/unlink operation for these models.
_STOCK_FORM_MODELS = {
    'stock.picking',
    'stock.move',
    'stock.move.line',
    'stock.quant',
    'stock.scrap',
    'stock.valuation.layer',
}


def _ensure_readonly_access(env):
    group = env.ref(
        'el_readonly_user.group_users_readonly', raise_if_not_found=False)
    if not group:
        return

    models = env['ir.model'].search([])
    ir_access = env['ir.model.access']
    for model in models:
        access = ir_access.search([
            ('group_id', '=', group.id),
            ('model_id', '=', model.id),
        ], limit=1)
        values = {
            'name': f'el_readonly_{model.model.replace(".", "_")}_read',
            'model_id': model.id,
            'group_id': group.id,
            'perm_read': True,
            'perm_write': (
                model.model in _READONLY_WRITABLE_MODELS
                or model.model in _STOCK_FORM_MODELS
            ),
            'perm_create': model.model in _READONLY_WRITABLE_MODELS,
            'perm_unlink': model.model in _READONLY_WRITABLE_MODELS,
        }
        if not access:
            ir_access.sudo().create(values)
        elif (
            access.perm_read != values['perm_read']
            or access.perm_write != values['perm_write']
            or access.perm_create != values['perm_create']
            or access.perm_unlink != values['perm_unlink']
        ):
            access.sudo().write(values)

    env.registry.clear_cache()


def post_init_hook(env):
    _ensure_readonly_access(env)


def post_update_hook(env):
    _ensure_readonly_access(env)
