import os
import jinja2


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(f'{os.path.dirname(__file__)}/templates/'),
    autoescape=jinja2.select_autoescape()
)

template = env.get_template('invoice.html')
template.render(test='some test here')
