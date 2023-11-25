import express from "express";
import helmet from 'helmet';
import bodyParser from "body-parser";
import cors from "cors";

// <-- Connections import -->
import mongo from "./connections/mongodb.js";
const app = express();
// <-- End of Connections import -->

// <-- Route Imports -->
import torrentRoutes from './routes/torrentRoutes.js';
// <-- End of Route Imports -->

// MongoDB connection
mongo();


// <-- Middleware -->
app.use(express.json());
app.use(helmet());
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true, 
}));
app.use(helmet.crossOriginResourcePolicy({ policy: "cross-origin" }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
// <-- End of Middleware -->

// <-- Routes -->
app.use("/torrent", torrentRoutes);
// <-- End of Routes -->


// Connection to port
const PORT = process.env.PORT || 6969;
app.listen(PORT, (err) => {
  if (err)
    throw err;
  console.log(`Server started on PORT ${PORT}...`);
});