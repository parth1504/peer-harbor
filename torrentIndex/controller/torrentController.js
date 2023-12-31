import TorrentModel from "../models/torrent.js";

const searchTorrent = async (req, res) => {
  const { query } = req.query;

  try {
    const torrents = await TorrentModel.find(
      { $text: { $search: query } },
      { score: { $meta: "textScore" } }
    ).sort({ score: { $meta: "textScore" } });

    res.json(torrents);
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
};

const serveTorrent = async (req, res) => {
  const { torrentId } = req.query;
  try {
    const torrent = await TorrentModel.findById(torrentId);

    if (!torrent) {
      return res.status(404).send("Torrent not found.");
    }

    res.set("Content-Type", "application/x-bittorrent");
    res.send(torrent.torrentFile);
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
};

const uploadTorrent = async (req, res) => {

  const tFile = req.file ? req.file.buffer : undefined;

  if (!tFile) {
    return res.status(400).send('No file uploaded');
  }

    const { name, keywords, createdBy, recipient} = req.body;
    console.log(req.body)
    const torrentFile = req.file.buffer;
    console.log(req.file);

    //console.log(torrentFile)
    try {
      const newTorrent = await TorrentModel.create({
        name,
        keywords,
        createdBy,
        torrentFile: Buffer.from(torrentFile, 'base64'),
      });

      res.status(201).json(newTorrent);
    } catch (error) {
      console.error(error);
      res.status(500).send('Internal Server Error');
    }
  };

export {searchTorrent, serveTorrent, uploadTorrent}