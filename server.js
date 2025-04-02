const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());

mongoose.connect('mongodb+srv://Twitterdb:CS4485.0W1@cluster0.toqut.mongodb.net/finished-data')
    .then(() => console.log("Database connected successfully"))
    .catch(err => console.log("Database connection error: ", err));

const dataSchema = mongoose.Schema({
    name: String,
    location: String,
    latitude: Number,
    longitude: Number,
    report: String,
    disaster_level: String,
    date: Date
});

const dataModel = mongoose.model("finalized-posts", dataSchema);

app.get("/getData", async (req, res) => {
    const Data = await dataModel.find();
    res.json(Data);
});

app.listen(3001, () => {
    console.log("Server is Running");
});
