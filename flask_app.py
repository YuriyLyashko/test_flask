from flask import Flask, request, render_template

from controller import data_for_html

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           regions=data_for_html.regions, selected_region=data_for_html.selected_region,
                           select_separator=data_for_html.select_separator)


@app.route('/', methods=['POST'])
def test():
    if request.method == 'POST':
        selected_region = request.form.get('name_selected')
        data_for_region = data_for_html.get_data_for_region(selected_region)
        return render_template('index.html',
                               regions=data_for_html.regions, data_for_region=data_for_region,
                               selected_region=selected_region,
                               select_separator=data_for_html.select_separator)


if __name__ == '__main__':
    app.run(debug=True)