from server import create_app
from celery import Celery

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=6969)

#     # Set up Celery configuration
# app.config['CELERY_BROKER_URL'] = 'pyamqp://guest:guest@localhost:5672//'
# app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

# # Initialize Celery with the Flask app
# celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# # Schedule the periodic task to update active peers (adjust the interval as needed)
# celery.conf.beat_schedule = {
#     'update-active-peers': {
#         'task': 'tasks.update_active_peers',
#         'schedule': 10,  # Every 10 seconds
#     },
# }

# celery.conf.timezone = 'UTC'