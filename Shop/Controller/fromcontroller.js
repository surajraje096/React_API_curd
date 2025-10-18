const form = require("../Schema/form");

// Create a new form entry
exports.createForm = async (req, res) => {
  try {
    const { name, email, age } = req.body;
    const newForm = new form({ name, email, age });
    await newForm.save();
    res.status(201).json(newForm);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};