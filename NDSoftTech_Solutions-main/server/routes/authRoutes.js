const express = require("express");
const router = express.Router();
const {register,login,googleLogin} = require("../controllers/authController");
const verifyFirebaseToken = require("../middlewares/verifyFirebaseToken");

router.post("/register", register);
router.post("/login", login);

router.post("/google-login", verifyFirebaseToken, googleLogin);

module.exports = router;
