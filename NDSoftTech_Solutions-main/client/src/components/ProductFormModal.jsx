import React, { useEffect, useState, useContext } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import { ProductContext } from "../context/ProductProvider";

const ProductFormModal = ({ show, onHide, editingProduct }) => {
  const { addProduct, updateProduct } = useContext(ProductContext);
  const [form, setForm] = useState({
    name: "",
    quantity: "",
    price: "",
    category: "",
  });

  useEffect(() => {
    if (editingProduct) {
      setForm(editingProduct);
    } else {
      setForm({
        name: "",
        quantity: "",
        price: "",
        category: "",
      });
    }
  }, [editingProduct]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    if (!form.name || !form.quantity || !form.price || !form.category) {
      alert("Fill all fields");
      return;
    }

    if (editingProduct) {
      updateProduct(form);
    } else {
      addProduct(form);
    }

    onHide();
  };

  const categories = ["Samsung", "Apple", "OnePlus", "Realme", "Xiaomi"];

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>
          {editingProduct ? "Edit Product" : "Add Product"}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Quantity</Form.Label>
            <Form.Control
              type="number"
              name="quantity"
              value={form.quantity}
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Price</Form.Label>
            <Form.Control
              type="number"
              name="price"
              value={form.price}
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Category</Form.Label>
            <Form.Select
              name="category"
              value={form.category}
              onChange={handleChange}
            >
              <option value="">Select</option>
              {categories.map((cat) => (
                <option key={cat}>{cat}</option>
              ))}
            </Form.Select>
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          {editingProduct ? "Update" : "Add"}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ProductFormModal;
