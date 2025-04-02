const { DISASTERS } = require("./data.js")

const { MongoClient } = require("mongodb");

const uri = "mongodb+srv://Twitterdb:CS4485.0W1@cluster0.toqut.mongodb.net/";
const client = new MongoClient(uri);

async function run() {
    try {
        await client.connect();
        console.log("Connected to MongoDB");

        const database = client.db("bluesky_db");
        const collection = database.collection("Cleaned_Data");
           // List all databases
           const databases = await client.db().admin().listDatabases();
           console.log("Databases:", databases.databases.map(db => db.name));
        // Fetch all documents (limit to 10 for testing)
       // const documents = await collection.find({}).limit(100).toArray();
        ////console.log("Fetched documents:", documents);
        //console.log("Fetched documents:", JSON.stringify(documents, null, 2));
        /*const db = client.db("finished-data");
        const collection2 = db.collection("finalized-posts");

         // Insert multiple documents
         const results = await collection2.insertMany(DISASTERS);
        
         console.log(`Inserted ${results.insertedCount} documents!`);
        */
        


        /*for (const dbInfo of databases.databases) {
            const dbName = dbInfo.name;
            console.log(`\n Exploring database: ${dbName}`);

            
            const db = client.db(dbName);
            const collections = await db.listCollections().toArray();
            console.log(`Collections in ${dbName}:`, collections.map(col => col.name));

            for (const collectionInfo of collections) {
                const collectionName = collectionInfo.name;
                console.log(`\n Collection: ${collectionName}`);

            
                const collection = db.collection(collectionName);
                const sampleDocuments = await collection.find({}).limit(3).toArray();
                
                console.log(`Sample documents from ${collectionName}:`, JSON.stringify(sampleDocuments, null, 2));
            }
        }*/
            

    } catch (error) {
        console.error("Error connecting to MongoDB:", error);
    } finally {
        await client.close();
    }
}

run();
