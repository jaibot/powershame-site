from powershame import app
import time

@app.template_filter('epoch_date_format')
def epoch_date( epoch ):
    return time.strftime( '%a, %b %d %Y', time.localtime(epoch) )

@app.template_filter('epoch_time_format')
def epoch_time( epoch ):
    return time.strftime( '%I:%M %p', time.localtime(epoch) )
