import os
import pexpect 
import shutil
import tempfile

from ansi2html import Ansi2HTMLConverter
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    # check for installation of style50
    if not os.path.isfile("style50/style50"):
        return render_template("error.html",
                               message="style50 is not properly installed.")

    if request.method == "GET":
        languages = ["c", "py", "js", "html", "css"]
        return render_template("index.html", languages=languages)
    else:
        code = request.form.get("code")
        language = request.form.get("language")

        if code == None or language == None:
            return render_template("error.html",
                                   message="Invalid request.")
        
        tempdir = tempfile.mkdtemp()
        filename = "{}/tmp.{}".format(tempdir, language)
        with open(filename, "w") as f:
            f.write(code)
        results = pexpect.run("style50/style50 {}".format(filename)).decode("utf-8")
        shutil.rmtree(tempdir)

        conv = Ansi2HTMLConverter()
        results = conv.convert(results)
        return results

