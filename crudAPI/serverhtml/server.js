const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect("mongodb://127.0.0.1:27017/testdb", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => console.log("✅ MongoDB connected"))
  .catch(err => console.error(err));

// User Schema
const userSchema = new mongoose.Schema({
  name: { type:String, required:true },
  email: { type:String, required:true, unique:true },
  address: { type:String, required:true }
});

const User = mongoose.model("User", userSchema);

// Routes
app.post("/api/users", async (req, res) => {
  try {
    const { name, email, address } = req.body;
    const newUser = new User({ name, email, address });
    await newUser.save();
    res.json({ message: "User saved successfully!", user: newUser });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.get("/api/users", async (req, res) => {
  const users = await User.find();
  res.json(users);
});

// Start server
app.listen(5000, () => console.log("🚀 Server running on http://localhost:5000"));