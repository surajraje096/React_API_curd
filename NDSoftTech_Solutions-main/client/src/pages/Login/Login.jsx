import React, { useState } from "react";
import axios from "axios";
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "../../firebase";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-toastify";

const Login = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/api/auth/login", form);
      localStorage.setItem("token", res.data.token);
      toast.success("Login successful");
      setTimeout(() => navigate("/"), 1500);
    } catch (err) {
      const msg = err.response?.data?.message || "Login failed";
      toast.error(msg);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const token = await result.user.getIdToken();

      const res = await axios.post(
        "http://localhost:5000/api/auth/google-login",
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );

      localStorage.setItem("token", res.data.token);
      toast.success("Google login successful");
      setTimeout(() => navigate("/"), 1500);
    } catch {
      toast.error("Google login failed");
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <form className="card p-4 shadow" onSubmit={handleLogin} style={{ width: 400 }}>
        <h3 className="text-center">Login</h3>
        <input
          type="email"
          name="email"
          placeholder="Email"
          className="form-control my-2"
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          className="form-control my-2"
          onChange={handleChange}
          required
        />
        <button className="btn btn-primary w-100">Login</button>
        <button
          type="button"
          onClick={handleGoogleLogin}
          className="btn btn-danger w-100 mt-2"
        >
          Login with Google
        </button>
        <p className="text-center mt-3">
          New user? <Link to="/register">Register</Link>
        </p>
      </form>
    </div>
  );
};

export default Login;
