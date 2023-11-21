import mongoose from 'mongoose';

const TorrentSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  keywords: [{
    type: String,
  }],
  dateCreated: {
    type: Date,
    default: Date.now,
  },
  createdBy: {
    type: String,
    required: true,
  },
  //Need to add a unique check.
  peerSet: [{
    type: String,
  }],
  torrentFile: {
    type: Buffer, 
    required: true,
  },
});

TorrentSchema.index({ name: 'text', keywords: 'text' });

const TorrentModel = mongoose.model('Torrent', TorrentSchema);

export default TorrentModel;
