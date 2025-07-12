"""
Main Flask application for managing environment configurations and GitLab Runner requests.

Provides routes to:
- Display a list of environments loaded from a configuration file.
- Submit requests for GitLab Runners via a web form.
- Confirm successful submission of runner requests.

Uses Flask-WTF for form handling and validation.

Author: Liora Milbaum
"""

import configparser

import flask

from manager import forms

app = flask.Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False


@app.route("/")
def show_environments():
    """
    Render the environments overview page.

    Reads environment configurations from 'environments.cfg' and
    passes the list of environments with their details to the template.
    """
    config = configparser.ConfigParser()
    config.read("manager/environments.cfg")
    environments = []
    for section in config.sections():
        env = {"name": section}
        env.update(config[section])
        environments.append(env)
    return flask.render_template("environments.html", environments=environments)


@app.route("/request-runner", methods=["GET", "POST"])
def request_runner():
    """
    Handle the GitLab Runner request form.

    - On GET: Render the request form.
    - On POST: Validate submitted form data.
      If valid, process the request and redirect to the success page.
      Otherwise, re-render the form with errors.

    The form captures environment name, project group, and optional tags.
    """
    form = forms.RequestForm()
    if form.validate_on_submit():
        environment_name = form.environment_name.data
        project_group = form.project_group.data
        tags = form.tags.data

        print(
            f"Requested GitLab Runner - Environment: {environment_name}, Group: {project_group}, Tags: {tags}"
        )

        return flask.redirect(flask.url_for("success"))

    return flask.render_template("request_runner.html", form=form)


@app.route("/success")
def success():
    """Display a confirmation message for successful GitLab Runner requests."""
    return "GitLab Runner request submitted successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
