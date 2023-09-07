from app import app,db
from app.models import User, Post

# imports the app variable that is a member of the app package

# decorator registers the function as a shell context function
# Function creates a shell context that adds database instance and models to the shell session
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}