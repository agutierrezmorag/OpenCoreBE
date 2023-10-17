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

const extractPromises = news_links.map(extractAndPushArticle);

Promise.all(extractPromises)
  .then(() => {
    // Save the articles in a JSON file
    const articlesFilePath = path.join(scriptDirectory, 'bun_jsons/articles.json');
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
    fs.writeFileSync(articlesFilePath, JSON.stringify(articles, null, 2));
  })
  .catch((error) => {
    console.error('Error extracting articles:', error);
  });

