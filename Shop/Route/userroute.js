const express = require('express');
const router = express.Router();
const userController = require('../Controller/usercontroller');

// Route to create a new user
router.post('/users', userController.createUser);

// Route to get all users
router.get('/users', userController.getAllUsers);

// Route to get a user by ID
router.get('/users/:id', userController.getUserById);

// Route to update a user by ID     
router.put('/users/:id', userController.updateUserById);

// Route to delete a user by ID
router.delete('/users/:id', userController.deleteUserById); 



module.exports = router;    