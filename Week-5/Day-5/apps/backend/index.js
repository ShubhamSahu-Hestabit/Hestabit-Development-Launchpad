const express = require('express');
const axios = require('axios');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json()); // CRUCIAL: To read JSON from the form

// 1. Models
const Stats = mongoose.model('Stats', new mongoose.Schema({ viewCount: Number }));
const Suggestion = mongoose.model('Suggestion', new mongoose.Schema({ 
    text: String, 
    date: { type: Date, default: Date.now } 
}));

// 2. DB Connection
mongoose.connect(process.env.MONGO_URI)
    .then(() => console.log("✅ DB Connected"))
    .catch(err => console.error("❌ DB Error", err));

// 3. GET Products + Increment Visits
app.get('/api/products', async (req, res) => {
    let stats = await Stats.findOne();
    if (!stats) stats = new Stats({ viewCount: 0 });
    stats.viewCount++;
    await stats.save();

    const response = await axios.get('https://dummyjson.com/products?limit=30');
    res.json({ products: response.data.products, totalVisits: stats.viewCount });
});

// 4. GET Suggestions (List)
app.get('/api/suggestions', async (req, res) => {
    const list = await Suggestion.find().sort({ date: -1 });
    res.json(list);
});

// 5. POST Suggestion (Form Submission)
app.post('/api/suggestions', async (req, res) => {
    const newEntry = new Suggestion({ text: req.body.text });
    await newEntry.save();
    res.json({ success: true });
});

app.get('/health', (req, res) => res.send('OK'));
app.listen(3000);