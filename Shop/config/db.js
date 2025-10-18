const mongoose = require("mongoose");
const dbURI = "mongodb://localhost:27017/mydatabase"; // Replace with your MongoDB URI

const connectDB = async () => {
  try {
    await mongoose.connect(dbURI, {
    
    });
   
    console.log("MongoDB connected successfully");
  } catch (err) {
    console.error("MongoDB connection error:", err.message);
    process.exit(1); // Exit process with failure
  }
}; // <-- Added missing closing bracket

module.exports = connectDB;