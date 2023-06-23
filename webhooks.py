import subprocess

from flask import Flask, abort, request

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhooks():
    branch_name = "refs/heads/master"
    if request.json["ref"] != branch_name:
        abort(400, f"Not the '{branch_name}' branch. Aborting update.")

    subprocess.call("update.sh")

    return "That is all folks!", 202
