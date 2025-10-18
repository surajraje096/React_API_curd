const mongoose = require("mongoose");

const productSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    quantity: { type: Number, required: true },
    price: { type: Number, required: true },
    category: { type: String, required: true },
    userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" }, 
  },
  { timestamps: true }
);

module.exports = mongoose.model("Product", productSchema);
