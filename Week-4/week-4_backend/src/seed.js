const mongoose = require('mongoose');
const config = require('../config');
const User = require('../models/User');
const Product = require('../models/Product');
 
async function seed() {
  await mongoose.connect(config.mongoUri);
 
  await User.create({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@test.com',
    password: '123456'
  });
 
  await Product.create({
    name: 'Test Product',
    price: 99,
    rating: 4
  });
 
  console.log('Seed data inserted');
  process.exit();
}
 
seed();