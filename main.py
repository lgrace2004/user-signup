
import webapp2
import cgi
import re

#html boilerplate
login_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style type="text/css">
        .error {
            color:red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Login</a>
    </h1>
</body>
</html>
<form method = "post">
    <label>
        Username
        <input type="text" name="username" value="%(uname)s"/>
        <span class="error">%(user_error)s</span>
        <br>
        Password
        <input type="password" name="password" value=""/>
        <span class="error"> %(password_error)s </span>
        <br>
        Verify Password
        <input type="password" name="verify_password" value=""/>
        <span class="error"> %(verify_error)s</span>
        <br>
        Email (Optional):
        <input type="text" name="email" value="%(user_email)s"/>
        <span class="error"> %(email_error)s </span>
        <br>
        <br>
        <input type="submit"/>
    </label>
</form>
"""



def valid_username(username):
    pattern = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    if pattern.match(username):
        return True
    return False

def valid_password(password):
    pattern = re.compile("^.{3,20}$")
    if pattern.match(password):
        return True
    return False

def valid_verify_password(password, verify_password):
    pattern = re.compile("^.{3,20}$")
    if (pattern.match(verify_password)) and (password == verify_password):
        return True
    return False


def valid_email(email):
    pattern = re.compile("^[\S]+@[\S]+.[\S]+$")
    if email == "":
        return True
    if pattern.match(email):
        return True
    return False


class MainHandler(webapp2.RequestHandler):

    def write_form(self, uname="", user_error="", password_error="",
                    verify_error="", user_email="", email_error=""):

                    self.response.write(login_form % {"uname":uname,
                    "user_error":user_error, "password_error":password_error,
                    "verify_error":verify_error, "user_email":user_email,
                     "email_error":email_error})



    def get(self):

        #error=self.request.get("user_error")
        #error_element = "<p class = 'error'>" + error + "</p>" if error else ""

        #combine pieces to build content of our response

        #self.response.write(content)
            self.write_form()





    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        verify_password = self.request.get("verify_password")
        email = self.request.get("email")

    #def error_write(self, error1, error2, error3, error4):

        user_reprimand= ""
        password_reprimand = ""
        verify_reprimand = ""
        email_reprimand = ""

        if valid_username(username) and valid_password(password) and valid_verify_password(password, verify_password) and valid_email(email):
            self.redirect("/welcome?username=%s" %username)
        else:
            if not valid_username(username):
                user_reprimand = "Invalid username"
            if not valid_password(password):
                password_reprimand = "Invalid password"
            else:
                if not valid_verify_password(password,verify_password):
                    verify_reprimand = "Passwords do not match"
            if not valid_email(email):
                email_reprimand = "Invalid email format"
            self.write_form(username, user_reprimand, password_reprimand, verify_reprimand, email, email_reprimand)




class Welcome(webapp2.RequestHandler):

    def get(self):

        username = self.request.get("username")
        content = " Welcome, " + username + "!"
        self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
