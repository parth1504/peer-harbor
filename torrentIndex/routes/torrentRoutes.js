import express from "express";
import { searchTorrent, serveTorrent, uploadTorrent } from "../controller/torrentController.js";
import multer from "multer";


const router = express.Router();

// <-- HTTP TORRENT SERVER ROUTES -->
const storage = multer.memoryStorage(); // Store files in memory
const upload = multer({ storage: storage });

// Search torrent by search query
router.get("/search", (req, res) => {
    searchTorrent(req, res);
})

// Serve torrent file to be downloaded
router.get("/serve", (req, res) => {
    serveTorrent(req, res);
})

// Upload Torrent file to http store
router.post("/upload", upload.single('torrentFile'), (req, res) => {
    uploadTorrent(req, res);
})

// <-- End of HTTP TORRENT SERVER ROUTES -->

export default router;