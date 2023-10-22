import { extract } from '@extractus/article-extractor'
const fs = require('fs');
const path = require('path');

const scriptDirectory = __dirname;

const newsLinksFilePath = path.join(scriptDirectory, 'bun_jsons/news_links.json');

const news_links = JSON.parse(fs.readFileSync(newsLinksFilePath));
const articles = [];

const extractAndPushArticle = async (link) => {
  const article = await extract(link);
  articles.push(article);
};

const saveArrayToJSON = (array, filePath, overwrite = false) => {
  let existingData = [];

  if (!overwrite) {
    try {
      const data = fs.readFileSync(filePath, 'utf8');
      existingData = JSON.parse(data);
    } catch (error) {
      console.error('Error reading existing data:', error);
    }
  }

  const newData = [...existingData, ...array];

  try {
    fs.writeFileSync(filePath, JSON.stringify(newData, null, 2));
    console.log('Data appended to JSON file successfully.');
  } catch (error) {
    console.error('Error writing data to JSON file:', error);
  }
}


const extractPromises = news_links.map(extractAndPushArticle);

Promise.all(extractPromises)
  .then(() => {
    // Save the articles in a JSON file
    const articlesFilePath = path.join(scriptDirectory, 'bun_jsons/articles.json');
    //remove from articles the ones that are already in the file based on the url
    return fs.promises.readFile(articlesFilePath, 'utf8')
      .then((data) => {
        const articlesInFile = JSON.parse(data);
        const articlesFileUrls = new Set(articlesInFile.map((article) => article.url));
        const articlesToSave = articles.filter((article) => !articlesFileUrls.has(article.url));
        //the articles follow this structure
        /*
        {
          url: String,
          title: String,
          description: String,
          image: String,
          author: String,
          favicon: String,
          content: String,
          published: Date String,
          source: String, // original publisher
          links: Array, // list of alternative links
          ttr: Number, // time to read in second, 0 = unknown
        }
        */
        saveArrayToJSON(articlesToSave, articlesFilePath, false);
      })
  })
  .catch((error) => {
    console.error('Error extracting articles:', error);
  });

