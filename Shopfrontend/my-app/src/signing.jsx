import React, { useState, useEffect } from "react";

const Signing = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    address: "",
  });

  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);
  const [editId, setEditId] = useState(null);
  const [editForm, setEditForm] = useState({ name: "", email: "", address: "" });

  // Fetch users on mount and after CRUD
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const res = await fetch("http://localhost:3000/api/users");
      const data = await res.json();
      setUsers(data);
    } catch {
      setUsers([]);
    }
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      const res = await fetch("http://localhost:3000/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        setMessage("Signed in successfully!");
        setForm({ name: "", email: "", address: "" });
        fetchUsers();
      } else {
        setMessage("Failed to sign in.");
      }
    } catch {
      setMessage("Error connecting to server.");
    }
  };

  // Edit handlers
  const handleEdit = (user) => {
    setEditId(user._id);
    setEditForm({ name: user.name, email: user.email, address: user.address });
  };

  const handleEditChange = (e) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleUpdate = async (id) => {
    await fetch(`http://localhost:3000/api/users/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(editForm),
    });
    setEditId(null);
    fetchUsers();
  };

  // Delete handler
  const handleDelete = async (id) => {
    await fetch(`http://localhost:3000/api/users/${id}`, { method: "DELETE" });
    fetchUsers();
  };

  return (
    <div style={{
         minHeight: "100vh",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      backgroundImage: "url('https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80')",
      backgroundSize: "cover",
      backgroundPosition: "center",
      backgroundRepeat: "no-repeat",
    }}>
      <form
        onSubmit={handleSubmit}
        style={{
          maxWidth: 350,
          margin: "60px auto 0 auto",
          padding: 24,
          borderRadius: 12,
          background: "#fff",
          boxShadow: "0 2px 8px rgba(0,0,0,0.07)"
        }}
      >
        <h2 style={{ fontSize: 22, marginBottom: 18 }}>Sign In</h2>
        <label style={{ fontSize: 15, marginBottom: 6, display: "block" }}>
          Name
        </label>
        <input
          type="text"
          name="name"
          value={form.name}
          onChange={handleChange}
          style={{ width: "100%", padding: 8, marginBottom: 16, fontSize: 15 }}
          required
        />
        <label style={{ fontSize: 15, marginBottom: 6, display: "block" }}>
          Email
        </label>
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          style={{ width: "100%", padding: 8, marginBottom: 16, fontSize: 15 }}
          required
        />
        <label style={{ fontSize: 15, marginBottom: 6, display: "block" }}>
          Address
        </label>
        <input
          type="text"
          name="address"
          value={form.address}
          onChange={handleChange}
          style={{ width: "100%", padding: 8, marginBottom: 20, fontSize: 15 }}
          required
        />
        <button
          type="submit"
          style={{
            width: "100%",
            padding: 10,
            fontSize: 16,
            background: "#4caf50",
            color: "#fff",
            border: "none",
            borderRadius: 6,
            cursor: "pointer"
          }}
        >
          Submit
        </button>
        {message && (
          <div style={{ marginTop: 14, fontSize: 14, color: "#333" }}>
            {message}
          </div>
        )}
      </form>
      

      {/* Users Table */}
      <div style={{ maxWidth: 700, margin: "30px auto 0 auto", background: "#fff", borderRadius: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.07)", padding: 20 }}>
        <h3 style={{ fontSize: 18, marginBottom: 10 }}>Users List</h3>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 15 }}>
          <thead>
            <tr style={{ background: "#f0f0f0" }}>
              <th style={{ padding: 8, border: "1px solid #ddd" }}>Name</th>
              <th style={{ padding: 8, border: "1px solid #ddd" }}>Email</th>
              <th style={{ padding: 8, border: "1px solid #ddd" }}>Address</th>
              <th style={{ padding: 8, border: "1px solid #ddd" }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) =>
              editId === user._id ? (
                <tr key={user._id}>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>
                    <input name="name" value={editForm.name} onChange={handleEditChange} style={{ width: "90%" }} />
                  </td>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>
                    <input name="email" value={editForm.email} onChange={handleEditChange} style={{ width: "90%" }} />
                  </td>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>
                    <input name="address" value={editForm.address} onChange={handleEditChange} style={{ width: "90%" }} />
                  </td>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>
                    <button onClick={() => handleUpdate(user._id)} style={{ marginRight: 8 }}>Save</button>
                    <button onClick={() => setEditId(null)}>Cancel</button>
                  </td>
                </tr>
              ) : (
                <tr key={user._id}>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>{user.name}</td>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>{user.email}</td>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>{user.address}</td>
                  <td style={{ padding: 8, border: "1px solid #ddd" }}>
                    <button onClick={() => handleEdit(user)} style={{ marginRight: 8 }}>Edit</button>
                    <button onClick={() => handleDelete(user._id)}>Delete</button>
                  </td>
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>

      <div style={{ width: "100%", textAlign: "center", marginBottom: 0 }}>
        <img
          src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
          alt="Tree Shadow Fog"
          style={{
            width: "100%",
            maxHeight: 180,
            objectFit: "cover",
            opacity: 0.85,
            borderBottomLeftRadius: 12,
            borderBottomRightRadius: 12
          }}
        />
      </div>
    </div>
  );
};

export default Signing;