    import express from 'express';
    import mongoose from 'mongoose';
    import bodyParser from 'body-parser';
     import dotenv from 'dotenv';
    import route from './routes/userRoute.js';
   
    
  const app = express();
  app.use(bodyParser.json());
  dotenv.config();
  
  const PORT = process.env.PORT || 8000;
  const MONGODBURL = process.env.MONGODB_URL; 

  mongoose.connect(MONGODBURL)
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));
        
    const itemSchema = new mongoose.Schema({
        name: String,
        quantity: Number
    });
    const Item = mongoose.model('Item', itemSchema);

    app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
    
    app.use("/api/user", route);
      

        



