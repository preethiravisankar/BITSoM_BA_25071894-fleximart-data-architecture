/********************************************
 Operation 1: Load Data 
Import the provided JSON file into collection 'products'
********************************************/
/* Import the provided JSON file into collection 'products' */

// Switch to fleximart database
db = db.getSiblingDB("fleximart");

// Read JSON file using mongosh-supported fs
const fs = require("fs");

const data = JSON.parse(
  fs.readFileSync(
    "part2-nosql/products_catalog.json",
    "utf8"
  )
);

// Insert data
if (Array.isArray(data)) {
  db.products.insertMany(data);
  print("Data imported successfully into fleximart.products");
} else {
  db.products.insertOne(data);
  print("Single document imported into fleximart.products");
}
/********************************************
 Operation 2: Basic Query 
 // Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
********************************************/

print("Running Electronics products query...");

//db = db.getSiblingDB("fleximart");

db.products.find(
  {
    category: "Electronics",
    price: { $lt: 50000 }
  },
  {
    _id: 0,
    name: 1,
    price: 1,
    stock: 1
  }
).forEach(printjson);

print("Query completed.");

/********************************************
 Operation 3: Review Analysis
 // Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array
********************************************/

print("Products with average rating >= 4.0");

db.products.aggregate([
  { $unwind: "$reviews" },
  {
    $group: {
      _id: "$product_id",
      name: { $first: "$name" },
      avg_rating: { $avg: "$reviews.rating" }
    }
  },
  {
    $match: {
      avg_rating: { $gte: 4.0 }
    }
  }
]).forEach(printjson);

print("Analysis completed.");

/********************************************
 Operation 4: Update Operation
 // Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
********************************************/

db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user: "U999",
        rating: 4,
        comment: "Good value",
        date: ISODate()
      }
    }
  }
);

/********************************************
 Operation 5: Complex Aggregation (3 marks)
 // Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending
********************************************/

db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: 1,
      product_count: 1
    }
  },
  {
    $sort: { avg_price: -1 }
  }

]);
