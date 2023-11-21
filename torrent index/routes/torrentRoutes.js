import express from "express";
import { searchTorrent, serveTorrent, uploadTorrent } from "../controller/torrentController";

const router = express.Router();

// <-- HTTP TORRENT SERVER ROUTES -->

// Search torrent by search query
router.get("/search", (req, res) => {
    searchTorrent(req, res);
})

// Serve torrent file to be downloaded
router.get("/serve", (req, res) => {
    serveTorrent(req, res);
})

// Upload Torrent file to http store
router.post("/upload", (req, res) => {
    uploadTorrent(req, res);
})

// <-- End of HTTP TORRENT SERVER ROUTES -->

export default router;