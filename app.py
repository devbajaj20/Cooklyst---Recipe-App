import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from extensions import db  # Import the db instance from extensions.py
from flask_migrate import Migrate
from models import Recipe, User, Comment, Message  # your SQLAlchemy models
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# App setup
app = Flask(__name__)
app.secret_key = 'ncfvhx5ri7678'  # You must set a secret key for sessions and flashing messages
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# ✅ MySQL database connection string (replace with your actual password)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Dev%40180404@localhost/recipe_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize extensions
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# ✅ Initialize SQLAlchemy with app
db.init_app(app)

# ✅ Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About Me', validators=[Length(max=300)])
    submit = SubmitField('Save Changes')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search']
        recipes = Recipe.query.filter(Recipe.title.contains(search_query)).all()
    else:
        recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/profile')
@login_required
def profile():
    user = current_user  # safer and recommended
    user_recipes = Recipe.query.filter_by(user_id=user.id).all()
    about_me = user.about_me if user.about_me else "No additional information"
    return render_template("profile.html", about_me=about_me, user_recipes=user_recipes)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        image = request.files.get('image')

        if not title or not ingredients or not instructions or not image:
            flash("All fields are required", "danger")
            return redirect(url_for('upload'))

        from werkzeug.utils import secure_filename  # make sure this is imported
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        new_recipe = Recipe(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            image=image_filename,
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()

        flash("Recipe uploaded successfully!", "success")
        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        content = request.form['content']
        rating = request.form.get('rating', type=int)

        comment = Comment(
            content=content,
            rating=rating,
            user_id=current_user.id,
            recipe_id=recipe.id
        )
        db.session.add(comment)
        db.session.commit()

        flash('Your comment has been added!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))

    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    return render_template('recipe_detail.html', recipe=recipe, comments=comments)

@app.route("/my_recipes")
@login_required
def my_recipes():
    user_recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template("my_recipes.html", recipes=user_recipes)

@app.route('/recipes')
def recipes():
    recipes = Recipe.query.options(joinedload(Recipe.user)).all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/submit-recipe', methods=['GET', 'POST'])
@login_required
def submit_recipe():
    if request.method == 'POST':
        # DEBUG: Log all form fields
        print("FORM DATA:", request.form)
        print("FILES:", request.files)

        title = request.form.get('title')
        description = request.form.get('description')
        cook_time = request.form.get('cook_time')
        serves = request.form.get('serves')
        ingredients = request.form.getlist('ingredients[]')
        steps = request.form.getlist('steps[]')
        image = request.files.get('image')

        # DEBUG: Log extracted values
        print("Title:", title)
        print("Image:", image)
        print("Ingredients:", ingredients)
        print("Steps:", steps)

        # Check required fields
        if not title or not image or not ingredients or not steps:
            flash('All fields are required.', 'danger')
            return redirect(request.url)

        if any(i.strip() == '' for i in ingredients) or any(s.strip() == '' for s in steps):
            flash('Each ingredient and step must be filled.', 'danger')
            return redirect(request.url)

        # Save the image
        from werkzeug.utils import secure_filename
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Convert lists to text
        ingredients_text = '\n'.join(ingredients)
        steps_text = '\n'.join(steps)

        # Create recipe
        new_recipe = Recipe(
            title=title,
            description=description,
            cook_time=cook_time,
            serves=serves,
            ingredients=ingredients_text,
            instructions=steps_text,
            image=image_filename,
            user_id=current_user.id
        )

        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('submit_recipe.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))

    return render_template('register.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user.image = filename  # Save the file name to the database

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('my_recipes'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid credentials.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/progress')
@login_required
def my_progress():
    user_id = current_user.id

    # Get all recipes created by the current user
    recipes = Recipe.query.filter_by(user_id=user_id).all()

    # Total number of saves (using many-to-many relationship)
    total_saves = sum(len(r.saved_by_users) for r in recipes)

    # Get all comments on user's recipes
    all_comments = Comment.query.join(Recipe).filter(Recipe.user_id == user_id).all()

    # Pie chart data: Saves per recipe
    saves_pie_data = {
        "labels": [r.title for r in recipes if r.title and r.saved_by_users],
        "values": [len(r.saved_by_users) for r in recipes if r.title and r.saved_by_users]
    }

    # Pie chart data: Comments per recipe
    comments_pie_data = {
        "labels": [r.title for r in recipes if r.title],
        "values": [len(r.comments) for r in recipes if r.title]
    }

    return render_template(
        "progress.html",
        total_saves=total_saves,
        total_comments=len(all_comments),
        comments=all_comments,
        saves_pie_data=saves_pie_data,
        comments_pie_data=comments_pie_data  # ✅ Corrected variable name
    )


@app.route('/save-recipe/<int:recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Check if the recipe is not already saved by the user
    if recipe not in current_user.saved:
        current_user.saved.append(recipe)
        db.session.commit()
        flash("Recipe saved!", "success")
    else:
        flash("You've already saved this recipe.", "warning")

    # Redirect back to the page the user came from
    return redirect(request.referrer)  # Redirects to the page that sent the POST request

@app.route('/saved-recipes')
@login_required
def saved_recipes():
    user = current_user
    recipes = user.saved  # Get all saved recipes for the current user
    return render_template('saved_recipes.html', recipes=recipes)

@app.route('/help', methods=['GET', 'POST'])
def help_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        content = request.form.get('message')

        new_msg = Message(name=name, email=email, content=content)
        db.session.add(new_msg)
        db.session.commit()

        flash("Your message has been sent!", "success")
        return redirect(url_for('help_page'))

    return render_template('help.html')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/edit-recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    # Retrieve the recipe by ID
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if the current user is the owner of the recipe
    if recipe.user_id != current_user.id:
        flash("You don't have permission to edit this recipe.")
        return redirect(url_for('my_recipes'))
    
    if request.method == 'POST':
        # Update recipe fields from form data
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        recipe.cook_time = request.form['cook_time']
        recipe.serves = request.form['serves']
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        
        # Handle file upload for image
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file:
                # Save the uploaded image to the specified directory
                image_filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                recipe.image = image_filename  # Update the recipe's image
        
        # Commit the updated recipe to the database
        db.session.commit()
        flash("Recipe updated successfully!")
        return redirect(url_for('my_recipes'))

    # Display the current recipe information in the form
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/unsave_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.saved:
        current_user.saved.remove(recipe)
        db.session.commit()
        flash('Recipe removed from saved list.', 'success')
    else:
        flash('Recipe was not in your saved list.', 'warning')
    return redirect(url_for('saved_recipes'))
# Initialize database and create folders
if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('static/uploads'):
            os.makedirs('static/uploads')
        db.create_all()  # Create the database tables if not already created
    app.run(debug=True)

