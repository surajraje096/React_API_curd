const express = require('express');
const app = express();
const connectDB = require('./config/db');
const userRoutes = require('./Route/userroute');
const cors = require('cors');
const fromRoutes = require('./Route/fromroute');

app.use(cors());


// Connect to the database
connectDB();    
const port = 3000;


// Middleware to parse JSON bodies
app.use(express.json());

// Use user routes
app.use('/api', userRoutes);
app.use('/api', fromRoutes);


app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

