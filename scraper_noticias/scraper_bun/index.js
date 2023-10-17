import { extract } from '@extractus/article-extractor'
const fs = require('fs')

//imort news_links.json and iterate over it
const news_links = JSON.parse(fs.readFileSync('./bun_jsons/news_links.json'))
const articles = []
for (const link of news_links) {
    //extract the article
    const article = await extract(link)
    //add the article to the array
    articles.push(article)
}

//save the articles in a json file
fs.writeFileSync('./bun_jsons/articles.json', JSON.stringify(articles))
