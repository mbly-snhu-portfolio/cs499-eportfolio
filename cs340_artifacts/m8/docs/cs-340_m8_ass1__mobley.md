# CS 340 Module Eight Assignment - MongoDB Advanced Query Operations

## Setup and Data Import

### Docker Environment
I created a Docker Compose file with MongoDB and MongoDB Express for this assignment:

```yaml
services:
  mongodb:
    image: mongo:latest
    container_name: cs-340-cs-340-mongodb-companies
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: P0werF!ex3123_
    volumes:
      - mongodb_data:/data/db
      - ./datasets:/datasets
    networks:
      - mongo-network

  mongo-express:
    image: mongo-express:latest
    container_name: cs-340-mongo-express-companies
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: P0werF!ex3123_
      ME_CONFIG_MONGODB_URL: mongodb://admin:P0werF!ex3123_@mongodb:27017/
    networks:
      - mongo-network
    depends_on:
      - mongodb

volumes:
  mongodb_data:

networks:
  mongo-network:
    driver: bridge
```

### Data Import
#### Run:
```bash
docker exec cs-340-mongodb-companies mongoimport --db companies --collection research --file /datasets/companies.json --username admin --password P0werF!ex3123_ --authenticationDatabase admin
```

Successfully imported 18,801 company documents from `companies.json` into the `companies.research` collection.


## Verification Queries

### Query 1: Find AdventNet

#### Query:
```javascript
db.research.find({"name" : "AdventNet"})
```

#### Run:
```bash
docker exec cs-340-mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"name\" : \"AdventNet\"})"
```

**Result:** Found 1 document for AdventNet (founded in 1996, server management software company).
(Screenshot)

### Query 2: Companies founded in 1996 (first 10 names)
#### Query:
```javascript
db.research.find({"founded_year" : 1996},{"name" : 1}).limit(10)
```
#### Run:
```bash
docker exec cs-340-mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"founded_year\" : 1996},{\"name\" : 1}).limit(10)"
```

#### Results:
1. AdventNet
2. RegOnline
3. LiveWorld
4. Shopzilla
5. LinkShare
6. MSNBC
7. TheStreet
8. Blucora
9. Omniture
10. Alexa

(screenshot)

## Assignment Tasks

### Task 1: Companies Founded After 2010 (First 20, Alphabetical Order)
#### Query:
```javascript
db.research.find(
  {"founded_year" : {$gt: 2010}},
  {"name": 1, "_id": 0}
).sort({"name": 1}).limit(20)
```
#### Run:
```bash
docker exec cs-340-mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"founded_year\" : {\$gt: 2010}}, {\"name\": 1, \"_id\": 0}).sort({\"name\": 1}).limit(20)"
```

#### Results:
1. 4shared
2. Advaliant
3. Advisor
4. Baveo
5. Bling Easy
6. Carfeine
7. CircleUp
8. Clowdy
9. CompareChecker
10. Cyphercor
11. DocASAP
12. Easel
13. EasyBib
14. Emotive Communications
15. FAT Media
16. FamilyDen
17. FirstString
18. Fixya
19. Fliggo
20. Fluc

(screenshot)

### Task 2: Companies with Offices in CA or TX (First 20, by Employee Count)
#### Query:
```javascript
db.research.find(
  {"offices.state_code": {$in: ["CA", "TX"]}},
  {"name": 1, "number_of_employees": 1, "_id": 0}
).sort({"number_of_employees": -1}).limit(20)
```
#### Run:
```bash
docker exec cs-340-mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"offices.state_code\": {\$in: [\"CA\", \"TX\"]}}, {\"name\": 1, \"number_of_employees\": 1, \"_id\": 0}).sort({\"number_of_employees\": -1}).limit(20)"
```
#### Results:
1. PayPal (300,000 employees)
2. Samsung Electronics (221,726 employees)
3. Accenture (205,000 employees)
4. Flextronics International (200,000 employees)
5. Safeway (186,000 employees)
6. Sony (180,500 employees)
7. Intel (86,300 employees)
8. Apple (80,000 employees)
9. Dell (80,000 employees)
10. ExxonMobil (76,900 employees)
11. Affiliated Computer Services (74,000 employees)
12. Cisco (63,000 employees)
13. Sun Microsystems (33,350 employees)
14. Texas Instruments (30,175 employees)
15. Google (28,000 employees)
16. The Walt Disney Company (25,000 employees)
17. Avaya (18,000 employees)
18. AMD (16,420 employees)
19. Experian (15,500 employees)
20. eBay (15,000 employees)

(screenshot)

### Task 3: Aggregation Pipeline - Total Offices by State (US Companies)
#### Query:
```javascript
db.research.aggregate([
  {$match: {"offices.country_code": "USA"}},
  {$unwind: "$offices"},
  {$match: {"offices.country_code": "USA"}},
  {$group: {"_id": "$offices.state_code", "total_offices": {$sum: 1}}},
  {$sort: {"total_offices": -1}}
])
```
#### Run:
```bash
docker exec cs-340-mongodb-companies mongosh --username admin --password password123 --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); var result = db.research.aggregate([{\$match: {\"offices.country_code\": \"USA\"}}, {\$unwind: \"\$offices\"}, {\$match: {\"offices.country_code\": \"USA\"}}, {\$group: {\"_id\": \"\$offices.state_code\", \"total_offices\": {\$sum: 1}}}, {\$sort: {\"total_offices\": -1}}]); result.toArray()""
```

**Explanation of the Aggregation Pipeline:**
1. **First $match**: Filters documents to only include companies that have at least one office in the USA
2. **$unwind**: Deconstructs the offices array, creating a separate document for each office
3. **Second $match**: Ensures we only count offices that are actually in the USA (additional filtering after unwind)
4. **$group**: Groups by state_code and counts the total number of offices per state
5. **$sort**: Sorts results by total_offices in descending order
6. **result.toArray()**: Prevents output from being paginated, showing all results

**Results (Top 10 States):**
1. CA (California): 3,903 offices
2. NY (New York): 1,084 offices
3. MA (Massachusetts): 623 offices
4. TX (Texas): 500 offices
5. WA (Washington): 415 offices
6. FL (Florida): 349 offices
7. IL (Illinois): 308 offices
8. VA (Virginia): 256 offices
9. (null): 252 offices (companies with no state specified)
10. CO (Colorado): 224 offices

(screenshot)

## Summary

This assignment demonstrates advanced MongoDB query operations including:
- **Basic queries** with filtering and projection
- **Sorting and limiting** results
- **Array queries** using the $in operator
- **Aggregation pipelines** with $match, $unwind, $group, and $sort operations
- **Complex document structure navigation** through nested arrays

The aggregation pipeline was particularly powerful for analyzing the office distribution across US states, showing that California has by far the most company offices (3,903), followed by New York (1,084) and Massachusetts (623).
