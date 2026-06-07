from odoo import models, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        project = super().create(vals)
        default_stages = ['New', 'In Progress', 'Approval One', 'Approval Two']
        stage_records = {}

        # إنشاء المراحل (Stages)
        for index, stage_name in enumerate(default_stages):
            stage = self.env['project.task.type'].create({
                'name': stage_name,
                'sequence': index,
                'project_ids': [(4, project.id)]
            })
            stage_records[stage_name] = stage

        # إنشاء المهام داخل المرحلة "New"
        if 'New' in stage_records:
            task_names = ['Site Visit', 'specification']
            for name in task_names:
                self.env['project.task'].create({
                    'name': name,
                    'project_id': project.id,
                    'stage_id': stage_records['New'].id,
                })

        return project
