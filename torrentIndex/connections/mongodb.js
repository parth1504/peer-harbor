import mongoose from "mongoose";
import 'dotenv/config';

// <--- MONGODB CONNECTION INITIATION --->

const mongo = async () => {
  try {
      mongoose.set('strictQuery', false);                              // Allows querying with undefined fields without generating errors.
      mongoose.connect(process.env.MongoDB);
    console.log("Connected to MongoDB Atlas");
  } catch (error) {
    console.log("Error connecting to MongoDB:", error);
  }
};

// <--- End of MONGODB CONNECTION INITIATION --->

export default mongo;