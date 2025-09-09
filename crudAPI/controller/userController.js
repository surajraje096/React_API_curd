import user from "../model/userModel.js";

export const create = async (req, res) => {
    try {
        const userData = new user(req.body);
        const {email} = userData;
       
        const existingUser = await user.findOne({email});
        if (existingUser) {
            return res.status(400).json({message: "User already exists"});
        }
        const savedUser = await userData.save();
        res.status(201).json(savedUser);
    } catch (error) {
        res.status(500).json('Internal Server Error');
    }
};

export const fetch = async (req, res) => {
    try
    {
       
        const users = await user.find({});
       if(users.length === 0)
       {
        return res.status(404).json({message: "No users found"});
       }
        res.status(200).json(users);
    }
    catch (error)
    {
        res.status(500).json('Internal Server Error');
    }
};

export const update = async (req, res) => {
    try {
        const  id  = req.params.id;
        const userExists = await user.findOne({_id: id});   
        if (!userExists) {
            return res.status(404).json({message: "User not found"});
        }
        const updatedUser = await user.findByIdAndUpdate(id, req.body, { new: true });
        res.status(200).json(updatedUser);
        
    } catch (error) {
        res.status(500).json('Internal Server Error');
    }
};

export const deleteUser = async (req, res) => {
    try {
        const  id  = req.params.id;
        const userExists = await user.findOne({_id: id});   
        if (!userExists) {
            return res.status(404).json({message: "User not found"});
        }
        await user.findByIdAndDelete(id);
        res.status(200).json({message: "User deleted successfully"});
        
    } catch (error) {
        res.status(500).json('Internal Server Error');
    }
};
