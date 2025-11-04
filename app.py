import psycopg2
import psycopg2.extras
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

# --- Configuration ---

app = Flask(__name__)

# A secret key is required for session management
app.config["SECRET_KEY"] = "your_very_secret_key_change_this"

# PostgreSQL Connection Details
# !! Replace with your own database details !!
DB_HOST = "172.31.25.211"
DB_NAME = "blog_db"
DB_USER = "postgres"
DB_PASS = "aman8180"


def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


# --- Routes ---


@app.route("/")
def home():
    """Redirects to the blog if logged in, else to the login page."""
    if "logged_in" in session:
        return redirect(url_for("blog"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles the login process."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        if not conn:
            flash("Database connection error. Please try again later.", "danger")
            return render_template("login.html")

        cursor = None
        try:
            # Use RealDictCursor to get results as dictionaries
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # --- DANGER ---
            # In a real app, you MUST hash and salt passwords.
            # This is only for a simple demo.
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password),
            )
            user = cursor.fetchone()

            if user:
                # User found, create session
                session["logged_in"] = True
                session["username"] = user["username"]
                return redirect(url_for("blog"))
            else:
                # User not found or password incorrect
                flash("Invalid username or password. Please try again.", "warning")

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # If GET request or login failed, show the login page
    return render_template("login.html")


@app.route("/blog")
def blog():
    """Displays the protected blog page."""
    if "logged_in" not in session:
        flash("You must be logged in to view this page.", "danger")
        return redirect(url_for("login"))

    # The blog content is now in the HTML template.
    # We just pass the username for the header.
    return render_template("blog.html", username=session.get("username"))


@app.route("/logout")
def logout():
    """Logs the user out by clearing the session."""
    session.pop("logged_in", None)
    session.pop("username", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# --- Run the App ---

if __name__ == "__main__":
    # bind to 0.0.0.0 so container exposes the app externally
    app.run(host="0.0.0.0", port=8000, debug=True)

