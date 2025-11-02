1. `docker exec mongodb-companies mongoimport --db companies --collection research --file /datasets/companies.json --username admin --password P0werF!ex3123_ --authenticationDatabase admin`

2. `docker exec -it mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin companies`

3. `docker exec mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"name\" : \"AdventNet\"})"`

4. `docker exec mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"founded_year\" : 1996},{\"name\" : 1}).limit(10)"`

5. `docker exec mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"founded_year\" : {\$gt: 2010}}, {\"name\": 1, \"_id\": 0}).sort({\"name\": 1}).limit(20)"`

6. `docker exec mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.find({\"offices.state_code\": {\$in: [\"CA\", \"TX\"]}}, {\"name\": 1, \"number_of_employees\": 1, \"_id\": 0}).sort({\"number_of_employees\": -1}).limit(20)"`

7. `docker exec mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); db.research.aggregate([{\$match: {\"offices.country_code\": \"USA\"}}, {\$unwind: \"\$offices\"}, {\$match: {\"offices.country_code\": \"USA\"}}, {\$group: {\"_id\": \"\$offices.state_code\", \"total_offices\": {\$sum: 1}}}, {\$sort: {\"total_offices\": -1}}])"`

8. `docker exec mongodb-companies mongosh --username admin --password P0werF!ex3123_ --authenticationDatabase admin --eval "db = db.getSiblingDB('companies'); var result = db.research.aggregate([{\$match: {\"offices.country_code\": \"USA\"}}, {\$unwind: \"\$offices\"}, {\$match: {\"offices.country_code\": \"USA\"}}, {\$group: {\"_id\": \"\$offices.state_code\", \"total_offices\": {\$sum: 1}}}, {\$sort: {\"total_offices\": -1}}]); result.toArray()"`