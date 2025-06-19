# Tree Plantation Social Tracker

A Django-based social platform for tracking tree plantation activities, inspired by Facebook's social feed. Users can register, log in, share trees, react, comment, and manage their profiles in a modern, interactive feed.

## Features

- **User Registration & Authentication**
  - Register, log in, and log out securely
  - Edit profile (username, email, password, profile picture)

- **Social Feed**
  - Public home page shows all tree posts from all users
  - Each post displays:
    - User avatar and name
    - Tree name, species, image, location, status, and last update
    - Reaction counts (👍 Like, ❤️ Love, 😮 Wow, 😢 Sad)
    - Comments with user info and timestamps
    - "Details" button to view full post
    - Delete button (only for the post owner)

- **Social Interactions**
  - React to any post directly from the feed (AJAX, no page reload)
  - Comment on any post directly from the feed (AJAX)
  - Only logged-in users can react, comment, or add trees

- **Tree Management**
  - Add new trees with images and structured location
  - Edit or delete your own tree posts
  - View detailed information for each tree

- **Profile Management**
  - Upload/change profile picture (avatar)
  - Edit username and email
  - Change password with confirmation

- **Modern UI/UX**
  - Responsive, card-based feed (Bootstrap)
  - User avatars (uploaded or auto-generated)
  - Login/Register buttons always visible in navbar
  - All posts visible to everyone; social actions require login

## Getting Started

1. **Clone the repository**
2. **Install dependencies** (in your virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
5. **Visit** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Folder Structure
- `tracker/` - Django project settings
- `trees/` - Main app (models, views, templates, forms)
- `media/` - Uploaded images (tree and profile pictures)
- `templates/` - HTML templates (feed, auth, profile, etc.)

## Notes
- Only logged-in users can add, react, comment, or delete posts.
- All posts are visible to everyone.
- Profile and password management are available from the profile page.

## License
MIT License
