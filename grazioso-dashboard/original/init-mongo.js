// MongoDB initialization script for AAC Animal Shelter project
// This script runs when the MongoDB container starts for the first time
// Also compatible with Apporto deployment where database may already exist

// Switch to admin database
db = db.getSiblingDB('admin');

// Create aacuser with proper permissions (only if user doesn't exist)
try {
  db.createUser({
    user: 'aacuser',
    pwd: 'SECRET',
    roles: [
      {
        role: 'readWrite',
        db: 'aac'
      },
      {
        role: 'dbAdmin',
        db: 'aac'
      }
    ]
  });
  print('Created aacuser successfully');
} catch (error) {
  if (error.code === 51003) {
    print('User aacuser already exists, skipping creation');
  } else {
    print('Error creating user: ' + error.message);
  }
}

// Switch to aac database
db = db.getSiblingDB('aac');

// Create animals collection (only if it doesn't exist)
try {
  db.createCollection('animals');
  print('Created animals collection');
} catch (error) {
  if (error.code === 48) {
    print('Collection animals already exists, skipping creation');
  } else {
    print('Error creating collection: ' + error.message);
  }
}

// Create indexes for better performance (only if they don't exist)
// Based on actual CSV structure: rec_num, age_upon_outcome, animal_id, animal_type, breed, color, date_of_birth, datetime, monthyear, name, outcome_subtype, outcome_type, sex_upon_outcome, location_lat, location_long, age_upon_outcome_in_weeks

try {
  db.animals.createIndex({ "animal_id": 1 }, { unique: true });
  print('Created unique index on animal_id');
} catch (error) {
  if (error.code === 85) {
    print('Index on animal_id already exists');
  } else {
    print('Error creating animal_id index: ' + error.message);
  }
}

try {
  db.animals.createIndex({ "rec_num": 1 });
  print('Created index on rec_num');
} catch (error) {
  if (error.code === 85) {
    print('Index on rec_num already exists');
  } else {
    print('Error creating rec_num index: ' + error.message);
  }
}

try {
  db.animals.createIndex({ "name": 1 });
  print('Created index on name');
} catch (error) {
  if (error.code === 85) {
    print('Index on name already exists');
  } else {
    print('Error creating name index: ' + error.message);
  }
}

try {
  db.animals.createIndex({ "animal_type": 1 });
  print('Created index on animal_type');
} catch (error) {
  if (error.code === 85) {
    print('Index on animal_type already exists');
  } else {
    print('Error creating animal_type index: ' + error.message);
  }
}

try {
  db.animals.createIndex({ "breed": 1 });
  print('Created index on breed');
} catch (error) {
  if (error.code === 85) {
    print('Index on breed already exists');
  } else {
    print('Error creating breed index: ' + error.message);
  }
}

try {
  db.animals.createIndex({ "outcome_type": 1 });
  print('Created index on outcome_type');
} catch (error) {
  if (error.code === 85) {
    print('Index on outcome_type already exists');
  } else {
    print('Error creating outcome_type index: ' + error.message);
  }
}

try {
  db.animals.createIndex({ "datetime": 1 });
  print('Created index on datetime');
} catch (error) {
  if (error.code === 85) {
    print('Index on datetime already exists');
  } else {
    print('Error creating datetime index: ' + error.message);
  }
}

print('MongoDB initialization completed successfully!');
print('Database: aac');
print('Collection: animals');
print('User: aacuser');
print('Indexes created for: animal_id, rec_num, name, animal_type, breed, outcome_type, datetime');
print('CSV fields supported: rec_num, age_upon_outcome, animal_id, animal_type, breed, color, date_of_birth, datetime, monthyear, name, outcome_subtype, outcome_type, sex_upon_outcome, location_lat, location_long, age_upon_outcome_in_weeks'); 