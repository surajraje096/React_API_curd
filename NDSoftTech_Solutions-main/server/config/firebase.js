const admin = require("firebase-admin");
const serviceAccount = require("./ndsoft-7944d-firebase-adminsdk-fbsvc-cd565e9c0c.json"); 

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

module.exports = admin;
