import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-toastify";

const Register = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    toast.info("Registering...");
    try {
      const res = await axios.post("http://localhost:5000/api/auth/register", form);
      localStorage.setItem("token", res.data.token);
      toast.success("Registered successfully");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      const msg = err.response?.data?.message || "Registration failed";
      toast.error(msg);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <form className="card p-4 shadow" onSubmit={handleRegister} style={{ width: 400 }}>
        <h3 className="text-center">Register</h3>
        <input type="text" name="name" placeholder="Name" className="form-control my-2" onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" className="form-control my-2" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" className="form-control my-2" onChange={handleChange} required />
        <button className="btn btn-success w-100">Register</button>
        <p className="text-center mt-3">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
};

export default Register;
