from app import create_app

# Create the Flask app using the application factory
app = create_app()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
