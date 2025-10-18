const mongoose = require("mongoose");

const schema = new mongoose.Schema({
  name: {
    type: String,
    
  },
  email: {
    type: String,
    
  },
  age: {
    type: Number,
   
    
  },


});




module.exports = mongoose.model("form", schema);