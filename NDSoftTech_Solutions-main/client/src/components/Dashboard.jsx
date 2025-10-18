import React, { useContext, useState } from "react";
import ProductFormModal from "./ProductFormModal";
import ProductList from "./ProductList";
import { ProductContext } from "../context/ProductProvider";
import { Button, Spinner } from "react-bootstrap";

const Dashboard = () => {
  const { loading } = useContext(ProductContext); 
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  const handleEdit = (product) => {
    setEditingProduct(product);
    setShowModal(true);
  };

  const handleAdd = () => {
    setEditingProduct(null);
    setShowModal(true);
  };

  return (
    <div className="container my-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3>📦 Inventory Dashboard</h3>
        <Button variant="primary" onClick={handleAdd}>
          ➕ Add Product
        </Button>
      </div>

      {loading ? (
        <div className="text-center my-5">
          <Spinner animation="border" role="status" variant="primary" />
          <p className="mt-3 text-muted">Loading products, please wait...</p>
        </div>
      ) : (
        <ProductList onEdit={handleEdit} />
      )}

      <ProductFormModal
        show={showModal}
        onHide={() => setShowModal(false)}
        editingProduct={editingProduct}
      />
    </div>
  );
};

export default Dashboard;
