const user = require('../models/user');  // Assuming the user model is correctly imported
const bcrypt = require('bcryptjs');      // Assuming you're using bcrypt for password hashing

// Function to handle errors
const handleErrors = (err) => {
    console.log(err.message, err.code);
    let errors = { email: '', password: '' };

    // Handle specific errors
    if (err.message.includes('User validation failed')) {
        if (err.message.includes('email')) {
            errors.email = 'That email is already registered';
        }
        if (err.message.includes('password')) {
            errors.password = 'Password must be at least 6 characters';
        }
    }

    // Return the error object
    return errors;
};

// Signup Route
const signup_post = async (req, res) => {
    const { mail, password } = req.body;
    
    // Validate the data before processing (e.g., check for empty fields)
    if (!mail || !password) {
        return res.status(400).json({ message: 'Please provide both email and password' });
    }

    try {
        // Check if user already exists
        const existingUser = await user.findOne({ mail });
        if (existingUser) {
            return res.status(409).json({ message: 'Email is already registered' });
        }

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create a new user
        const newUser = await user.create({ mail, password: hashedPassword });

        // Send success response
        res.status(200).json({ message: 'Signup successful', user: newUser });
    } catch (err) {
        const errors = handleErrors(err);
        res.status(400).json({ message: 'Error occurred during signup', error: errors });
    }
};

// Login Route
const login_post = async (req, res) => {
    const { mail, password } = req.body;

    // Validate the data before processing
    if (!mail || !password) {
        return res.status(400).json({ message: 'Please provide both email and password' });
    }

    try {
        // Find the user by email
        const user = await user.findOne({ mail });
        if (!user) {
            return res.status(400).json({ message: 'No user found with that email' });
        }

        // Compare the entered password with the stored hashed password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ message: 'Incorrect password' });
        }

        // Send success response
        res.status(200).json({ message: 'Login successful', user: user._id });
    } catch (err) {
        res.status(500).json({ message: 'Server error', error: err.message });
    }
};

module.exports = { signup_post, login_post };
