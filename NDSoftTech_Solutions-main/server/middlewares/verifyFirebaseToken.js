const admin = require("../config/firebase");

const verifyFirebaseToken = async (req, res, next) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).json({ message: "No token provided" });

  try {
    const decoded = await admin.auth().verifyIdToken(token);
    req.firebaseUser = decoded;
    next();
  } catch (err) {
    res.status(401).json({ message: "Invalid Firebase token" });
  }
};

module.exports = verifyFirebaseToken;
