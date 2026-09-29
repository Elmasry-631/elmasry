# Data Flow

Source model state change -> mobile.webhook.event.create -> cron signs immutable payload -> HTTPS POST -> sent or retry schedule.