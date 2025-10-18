const Product = require("../models/Product");

exports.getProducts = async (req, res) => {
  try {
    const products = await Product.find().sort({ createdAt: -1 });
    res.status(200).json(products);
  } catch (error) {
    console.error("Error fetching products:", error.message);
    res.status(500).json({ message: "Server error while fetching products" });
  }
};

exports.createProduct = async (req, res) => {
  try {
    const { name, quantity, price, category } = req.body;

    if (!name || !quantity || !price || !category) {
      return res.status(400).json({ message: "All fields are required" });
    }

    const newProduct = new Product({ name, quantity, price, category });
    await newProduct.save();

    res.status(201).json({
      message: "Product created successfully",
      product: newProduct,
    });
  } catch (error) {
    console.error("Error creating product:", error.message);
    res.status(500).json({ message: "Server error while creating product" });
  }
};

exports.updateProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, quantity, price, category } = req.body;

    const product = await Product.findById(id);
    if (!product)
      return res.status(404).json({ message: "Product not found" });

    product.name = name ?? product.name;
    product.quantity = quantity ?? product.quantity;
    product.price = price ?? product.price;
    product.category = category ?? product.category;

    const updatedProduct = await product.save();

    res.status(200).json({
      message: "Product updated successfully",
      product: updatedProduct,
    });
  } catch (error) {
    console.error("Error updating product:", error.message);
    res.status(500).json({ message: "Server error while updating product" });
  }
};

exports.deleteProduct = async (req, res) => {
  try {
    const { id } = req.params;

    const product = await Product.findById(id);
    if (!product)
      return res.status(404).json({ message: "Product not found" });

    await product.deleteOne();

    res.status(200).json({ message: "Product deleted successfully" });
  } catch (error) {
    console.error("Error deleting product:", error.message);
    res.status(500).json({ message: "Server error while deleting product" });
  }
};
