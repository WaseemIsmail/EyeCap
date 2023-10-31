const express = require('express')

// controller functions
const { signupUser, loginUser, getUserdetails, updateUserdetails, deleteUserdetails, listAllUsers } = require('../controllers/userController')

const router = express.Router()

// login route
router.post('/login', loginUser)

// signup route
router.post('/signup', signupUser)

// profile route
router.get('/profile/:id', getUserdetails)

// profile route
router.patch('/profile/:id', updateUserdetails)

// profile route
router.delete('/profile/:id', deleteUserdetails)

// admin panel
router.get('/admincp', listAllUsers)

module.exports = router