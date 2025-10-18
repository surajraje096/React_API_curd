const express = require('express');
const router = express.Router();
const fromcontroller = require('../Controller/fromcontroller');


// Route to create a new form entry
router.post('/form', fromcontroller.createForm);    

module.exports = router;
