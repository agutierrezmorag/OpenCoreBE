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
    fs.writeFileSync(articlesFilePath, JSON.stringify(articles));
  })
  .catch((error) => {
    console.error('Error extracting articles:', error);
  });

