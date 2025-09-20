import express from 'express';
import { fetch, create , update , deleteUser, getUserById }  from "../controller/userController.js";

const route = express.Router();

route.post("/create", create);
route.get("/getAllUsers", fetch);
route.put("/update/:id", update);
route.delete("/delete/:id", deleteUser);
route.get("/ById/:id", getUserById);


export default route;