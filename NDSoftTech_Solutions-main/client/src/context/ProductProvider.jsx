import React, { createContext, useEffect, useState } from "react";
import API from "../api";
import { toast } from "react-toastify";

export const ProductContext = createContext();

export const ProductProvider = ({ children }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const productsPerPage = 5;

  useEffect(() => {
    getProducts();
  }, []);

  const getProducts = async () => {
    setLoading(true);
    try {
      const res = await API.get("/products");
      setProducts(res.data);
    } catch (err) {
      toast.error("Failed to load products.", { toastId: "load-error" });
    } finally {
      setLoading(false);
    }
  };

  const addProduct = async (product) => {
    try {
      const res = await API.post("/products", product);
      setProducts([res.data.product, ...products]);
      setCurrentPage(1);
      toast.success("Product added successfully");
    } catch (err) {
      toast.error("Failed to add product.");
    }
  };

  const updateProduct = async (product) => {
    try {
      const res = await API.put(`/products/${product._id}`, product);
      const updated = products.map((p) =>
        p._id === product._id ? res.data.product : p
      );
      setProducts(updated);
      toast.success("Product updated");
    } catch (err) {
      toast.error("Failed to update product.");
    }
  };

  const deleteProduct = async (id) => {
    try {
      await API.delete(`/products/${id}`);
      const filtered = products.filter((p) => p._id !== id);
      setProducts(filtered);
      toast.success("Product deleted");
    } catch (err) {
      toast.error("Failed to delete product.");
    }
  };

  const filtered = products.filter((p) => {
    const matchName = p.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchCategory = filterCategory ? p.category === filterCategory : true;
    return matchName && matchCategory;
  });

  const indexLast = currentPage * productsPerPage;
  const indexFirst = indexLast - productsPerPage;
  const currentProducts = filtered.slice(indexFirst, indexLast);
  const totalPages = Math.ceil(filtered.length / productsPerPage);

  return (
    <ProductContext.Provider
      value={{
        loading, products, currentProducts, currentPage, setCurrentPage, totalPages,
        addProduct, updateProduct, deleteProduct, searchTerm, setSearchTerm,
        filterCategory, setFilterCategory
      }}
    >
      {children}
    </ProductContext.Provider>
  );
};
